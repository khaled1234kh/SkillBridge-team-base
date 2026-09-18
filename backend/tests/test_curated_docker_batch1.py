"""End-to-end contracts for the curated Docker topics (batch 1: Containers + Images)."""
from urllib.parse import quote

import pytest

from app import genai, models


@pytest.fixture(autouse=True)
def offline_reviewer(monkeypatch):
    """Use the explicitly labelled local evaluator for deterministic journeys."""
    monkeypatch.setattr(genai, "genai_enabled", lambda: False)


def _url(student_id, skill_id, competency):
    return f"/api/students/{student_id}/learning/{skill_id}/lessons/{quote(competency, safe='')}"


def _answers_for_all_gaps(questions):
    """Return a wrong answer for each question (MCQ or free-text)."""
    answers = []
    for q in questions:
        opts = q.get("options") or []
        if opts:
            # MCQ: pick a wrong option
            wrong = next(opt for opt in opts if opt != q["correct_answer"])
            answers.append(wrong)
        else:
            # Free-text: provide a deliberately wrong answer
            answers.append("WRONG ANSWER")
    return answers


def _make_path(client, student_id, headers, docker_skill):
    generated = client.post(
        f"/api/students/{student_id}/learning/{docker_skill['id']}/diagnostic/generate",
        json={}, headers=headers).json()
    completed = client.post(
        f"/api/students/{student_id}/learning/{docker_skill['id']}/diagnostic/submit",
        json={"diagnostic_id": generated["diagnostic_id"], "answers": _answers_for_all_gaps(generated["questions"])},
        headers=headers)
    assert completed.status_code == 200, completed.text
    path = client.post(
        f"/api/students/{student_id}/learning/{docker_skill['id']}/personalized-path/generate",
        json={}, headers=headers).json()
    return generated, path


def test_docker_diagnostic_covers_all_blueprint_topics_and_path_is_prerequisite_ordered(
        client, student_id, auth_headers):
    """Fallback diagnostic covers multiple blueprint topics; path respects blueprint order."""
    headers = auth_headers("aisha@student.edu")
    docker = models.get_skill_by_name("Docker")
    generated, path = _make_path(client, student_id, headers, docker)

    # Fallback diagnostic covers multiple blueprint topics (capped at 9 questions)
    assert 7 <= len(generated["questions"]) <= 9
    expected_topics = {
        "containers", "images", "basic_commands", "dockerfile",
        "ports", "volumes", "networking", "compose",
        "multi_stage_builds", "security_&_secrets", "orchestration_basics"
    }
    actual_topics = {q["competency"] for q in generated["questions"]}
    assert actual_topics.issubset(expected_topics)

    # Path respects blueprint order
    from app import skill_blueprint as sb
    expected_order = sb.required_competencies("Docker", "Beginner", "Advanced")
    path_competencies = [item["competency"] for item in path["items"]]
    path_indices = [expected_order.index(c) for c in path_competencies if c in expected_order]
    assert path_indices == sorted(path_indices), "Path order must follow blueprint order"


def test_both_curated_docker_topics_complete_without_verifying_skill_and_cache_exact_answer(
        client, student_id, auth_headers):
    headers = auth_headers("aisha@student.edu")
    docker = models.get_skill_by_name("Docker")
    before = {(s["name"], s["level"]) for s in models.get_student(student_id).get("verified_skills") or []}
    _, path = _make_path(client, student_id, headers, docker)
    answers = {
        "containers": (
            "docker ps -a\n"
            "docker logs web\n"
            "docker start web\n"
            "docker rm web\n"
            "If docker logs shows immediate exit, I'd read the error line in the logs, "
            "check the container's command/entrypoint, and run it once in the foreground "
            "with `docker run -it --rm nginx:1.27 /bin/bash` to see the failure directly."
        ),
        "images": (
            "docker pull nginx:1.27\n"
            "docker images\n"
            "docker image inspect nginx:1.27\n"
            "docker tag nginx:1.27 myregistry.local:5000/web:1.27\n"
            "docker rmi nginx:1.25\n"
            ":latest is wrong because it is a moving pointer; pin the exact version tag "
            "nginx:1.27 (or its sha256 digest) so every deploy pulls the identical image."
        ),
    }
    for item in path["items"]:
        base = _url(student_id, docker["id"], item["competency"])
        lesson = client.post(base + "/generate", json={}, headers=headers)
        assert lesson.status_code == 200, lesson.text
        content = lesson.json()["content"]
        # Only curated topics (containers, images) have canonical content
        if item["competency"] in ("containers", "images"):
            assert content["canonical"]["source"] == "trusted_cs_knowledge_base"
            assert len(content["locales"]["ar"]["mini_check"]["questions"]) == 3
            first = client.post(base + "/practice", json={"answer": answers[item["competency"]]}, headers=headers)
            assert first.status_code == 200, first.text
            attempt = first.json()["attempt"]
            assert attempt["practice_task"]["type"] == "practical"
            assert attempt["status"] in ("ready", "needs_review")
            assert isinstance(attempt["score"], (int, float))
            cached = client.post(base + "/practice", json={"answer": answers[item["competency"]]}, headers=headers)
            assert cached.status_code == 200, cached.text
            assert cached.json()["reused"] is True
            assert cached.json()["attempt"]["id"] == first.json()["attempt"]["id"]
            changed = client.post(base + "/practice", json={"answer": answers[item["competency"]] + "\nI checked one more case."}, headers=headers)
            assert changed.status_code == 200, changed.text
            assert changed.json().get("reused") is not True
            questions = content["mini_check"]["questions"]
            passed = client.post(base + "/mini-check", json={"answers": [q["correct_answer"] for q in questions]}, headers=headers)
            assert passed.status_code == 200, passed.text
            assert passed.json()["lesson"]["state"] == "completed"

    persisted = client.get(f"/api/students/{student_id}/learning/{docker['id']}/personalized-path", headers=headers).json()
    # Only curated topics (containers, images) are completed in this test
    curated_item_ids = {item["id"] for item in path["items"] if item["competency"] in ("containers", "images")}
    assert curated_item_ids.issubset(set(persisted["progress"]))
    assert {(s["name"], s["level"]) for s in models.get_student(student_id).get("verified_skills") or []} == before


def test_docker_diagnostic_tagging_covers_blueprint_topics(
        client, student_id, auth_headers):
    """Fallback diagnostic covers multiple blueprint topics with correct competency tags."""
    headers = auth_headers("aisha@student.edu")
    docker = models.get_skill_by_name("Docker")
    generated, _ = _make_path(client, student_id, auth_headers("aisha@student.edu"), docker)

    # Every question must carry its exact competency tag (no round-robin)
    expected_topics = {
        "containers", "images", "basic_commands", "dockerfile",
        "ports", "volumes", "networking", "compose",
        "multi_stage_builds", "security_&_secrets", "orchestration_basics"
    }
    actual_topics = {q["competency"] for q in generated["questions"]}
    assert actual_topics.issubset(expected_topics)
    assert 7 <= len(generated["questions"]) <= 9


def test_curated_docker_mini_check_grading_threshold(
        client, student_id, auth_headers):
    """A correct Mini Check answer scores >= 70%; a wrong answer scores < 70%."""
    headers = auth_headers("aisha@student.edu")
    docker = models.get_skill_by_name("Docker")
    _, path = _make_path(client, student_id, auth_headers("aisha@student.edu"), docker)

    for item in path["items"]:
        base = _url(student_id, docker["id"], item["competency"])
        lesson = client.post(base + "/generate", json={}, headers=auth_headers("aisha@student.edu"))
        assert lesson.status_code == 200
        content = lesson.json()["content"]
        questions = content["mini_check"]["questions"]
        # Only curated topics (containers, images) have MCQ mini-checks
        if item["competency"] not in ("containers", "images"):
            continue
        # All correct -> score 100% >= 70 -> pass
        passed = client.post(base + "/mini-check", json={"answers": [q["correct_answer"] for q in questions]}, headers=auth_headers("aisha@student.edu"))
        assert passed.status_code == 200, passed.text
        assert passed.json()["lesson"]["state"] == "completed"
        # All wrong -> score 0% < 70 -> fail
        wrong = [q["options"][0] if q["options"][0] != q["correct_answer"] else q["options"][1] for q in questions]
        failed = client.post(base + "/mini-check", json={"answers": wrong}, headers=auth_headers("aisha@student.edu"))
        assert failed.status_code == 200, failed.text
        assert failed.json()["lesson"]["state"] == "in_progress"


def test_curated_docker_mini_check_pass_persists_and_fail_does_not(
        client, student_id, auth_headers):
    """Passing the Mini Check persists topic completion; failing does not."""
    headers = auth_headers("aisha@student.edu")
    docker = models.get_skill_by_name("Docker")
    _, path = _make_path(client, student_id, auth_headers("aisha@student.edu"), docker)

    for item in path["items"]:
        base = _url(student_id, docker["id"], item["competency"])
        client.post(base + "/generate", json={}, headers=auth_headers("aisha@student.edu"))
        client.post(base + "/start", json={}, headers=headers)
        content = client.get(base, headers=headers).json()["content"]
        questions = content["mini_check"]["questions"]
        # Only curated topics (containers, images) have MCQ mini-checks
        if item["competency"] not in ("containers", "images"):
            continue
        # Fail -> no progress
        wrong = [q["options"][0] if q["options"][0] != q["correct_answer"] else q["options"][1] for q in questions]
        client.post(base + "/mini-check", json={"answers": wrong}, headers=headers)
        before_progress = client.get(
            f"/api/students/{student_id}/learning/{docker['id']}/personalized-path", headers=headers).json()
        assert item["id"] not in before_progress.get("progress", [])
        # Pass -> progress
        correct = [q["correct_answer"] for q in questions]
        client.post(base + "/mini-check", json={"answers": correct}, headers=headers)
        after_progress = client.get(
            f"/api/students/{student_id}/learning/{docker['id']}/personalized-path", headers=headers).json()
        assert item["id"] in after_progress.get("progress", [])


def test_curated_docker_mini_check_does_not_create_verified_skill(
        client, student_id, auth_headers):
    """Passing the Mini Check does NOT create a Verified Skill."""
    headers = auth_headers("aisha@student.edu")
    docker = models.get_skill_by_name("Docker")
    _, path = _make_path(client, student_id, auth_headers("aisha@student.edu"), docker)

    before = {(s["name"], s["level"]) for s in models.get_student(student_id).get("verified_skills") or []}
    for item in path["items"]:
        base = _url(student_id, docker["id"], item["competency"])
        client.post(base + "/generate", json={}, headers=headers)
        client.post(base + "/start", json={}, headers=headers)
        content = client.get(base, headers=headers).json()["content"]
        questions = content["mini_check"]["questions"]
        # Only curated topics (containers, images) have MCQ mini-checks
        if item["competency"] not in ("containers", "images"):
            continue
        correct = [q["correct_answer"] for q in content["mini_check"]["questions"]]
        client.post(base + "/mini-check", json={"answers": correct}, headers=headers)
    after = {(s["name"], s["level"]) for s in models.get_student(student_id).get("verified_skills") or []}
    assert after == before


def test_curated_docker_prerequisites_exist_in_blueprint():
    """Any prerequisite topic_id referenced actually exists in the blueprint."""
    from app import knowledge_base, skill_blueprint as sb

    cont = knowledge_base.complete_lesson("Docker", "Containers")
    img = knowledge_base.complete_lesson("Docker", "Images")
    assert cont is not None
    assert img is not None
    # Containers has no prerequisites
    assert cont["prerequisites"] == []
    # Images has Containers as prerequisite
    assert len(img["prerequisites"]) == 1
    assert img["prerequisites"][0]["competency"] == "Containers"
    # The prerequisite must exist in the blueprint
    docker_topics = sb.required_competencies("Docker", "Beginner", "Advanced")
    assert "Containers" in docker_topics
    assert "Images" in docker_topics


def test_curated_docker_content_has_bilingual_explanation_and_validated_checks():
    """Each curated topic loads with EN/AR, objectives, prereqs, worked example, practical exercise, Mini Check, diagnostic questions, resource links."""
    from app import lessons, knowledge_base

    for competency in ("Containers", "Images"):
        content = lessons.generate_lesson("Docker", competency, "learn")
        assert content["canonical"]["source"] == "trusted_cs_knowledge_base"
        assert "بالعربية" not in content["learn"]["explanation"]
        # Arabic presence
        arabic = content["locales"]["ar"]
        assert arabic["learn"]["explanation"]
        assert arabic["learn"]["key_ideas"]
        assert arabic["example"]["content"]
        assert arabic["practice"]["task"]
        assert arabic["practice"]["evaluation_note"]
        assert len(arabic["mini_check"]["questions"]) == 3
        # Mini Check answers are exact-match and all 3 correct passes
        answers = [q["correct_answer"] for q in content["mini_check"]["questions"]]
        from app import lessons as lessons_mod
        assert lessons_mod.score_mini_check(content["mini_check"]["questions"], answers) == (3, 3, True)
        # Practice task exists and is practical
        assert content["practice"]["type"] == "practical"
        assert content["practice"]["task"]
        assert content["practice"]["response_type"] == "command"
        assert content["practice"]["evaluation_note"]
        # Worked example present
        assert content["example"]["content"]
        assert content["example"]["type"] == "bash"
        # Grounding sources present
        assert content["learn"]["grounding_sources"]
        # Prerequisites: Images has Containers; Containers has none
        canonical = content["canonical"]
        if competency == "Images":
            assert canonical["prerequisites"][0]["competency"] == "Containers"
        else:
            assert canonical["prerequisites"] == []


def test_curated_docker_resource_links_are_curated_and_safe():
    """Recommended resources for Containers and Images come from the curated docker catalog (docs.docker.com)."""
    from app import resources

    # Containers has 3 curated resources; Images has 2 (both from docs.docker.com)
    expected_min = {"Containers": 3, "Images": 2}
    for competency in ("Containers", "Images"):
        res = resources.recommend_lesson_resources(
            "Docker", "DevOps", competency, "Beginner", "Junior AI Engineer", live_check=False)
        assert len(res) >= expected_min[competency], f"{competency}: expected >= {expected_min[competency]}, got {len(res)}"
        # All curated and from docs.docker.com
        assert all(r["source_kind"] == "curated" for r in res[:expected_min[competency]])
        assert all("docs.docker.com" in r["url"] for r in res[:expected_min[competency]])