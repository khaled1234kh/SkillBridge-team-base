"""Small, curated CS knowledge base used by the Learning system.

This module is deliberately data-first: canonical curriculum, prerequisites, and
lesson facts live here, never in an LLM prompt.  Only entries marked ``complete``
can be served as a canonical lesson.  Planned entries document the extension
shape without pretending that their content has shipped.
"""
from copy import deepcopy
import re


KNOWLEDGE_BASE_VERSION = "cs-kb-v2"


def _key(value):
    # Competencies are persisted both as display labels and as path identifiers
    # (for example ``python_error_handling``).  Treat those representations as
    # the same canonical lookup key so a stored path cannot fall back to a
    # generic generated lesson.
    return re.sub(r"\s+", " ", str(value or "").replace("_", " ").strip()).lower()


PYTHON_FUNCTIONS = {
    "status": "complete",
    "skill_aliases": ("python", "python programming"),
    "competency": "Python Functions",
    "objective": "Define a Python function with parameters and return a reusable value.",
    "prerequisites": [
        {
            "competency": "Python values, variables, and expressions",
            "relationship": "required foundation",
            "why": "Function arguments and return values are ordinary Python values; you need to read assignments and expressions to follow a function call.",
        },
    ],
    "roadmap_rationale": (
        "Python Functions appears in this roadmap because it is the first reusable-unit skill: "
        "it lets you turn repeated steps into a named, testable behavior. The canonical Python "
        "curriculum places it after values, variables, and expressions, not because a role demands it."
    ),
    "learn": {
        "title": "Python Functions",
        "explanation": (
            "A **function** is a named recipe for a small job. `def` creates the recipe, "
            "parameters receive input, and `return` sends a result back to the caller."
        ),
        "key_ideas": [
            "Define a function with `def name(parameters):` and an indented body.",
            "Arguments are the values supplied at a call; parameters are the names inside the definition.",
            "Use `return` when later code needs the computed value; `print` only displays text.",
            "Keep one function focused on one clear responsibility so it is easy to test and reuse.",
        ],
        "key_terms": {
            "function": "A named block of reusable code.",
            "parameter": "A variable in the function definition that receives an input.",
            "argument": "A concrete value passed when calling a function.",
            "return value": "The value a function sends back to its caller.",
        },
        "job_relevance": "Functions make small pieces of application, data, and automation code reusable and independently testable.",
        "common_mistake": "Do not confuse `print(total)` with `return total`: printed output cannot be used by the next line of program logic.",
        "worked_example": "The example calculates a delivery total from two inputs, then checks the returned value with several inputs.",
        "depth_note": "Canonical beginner content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": "Examples use Python 3 syntax and the standard library only.",
        "grounding_sources": [{"title": "Python tutorial: defining functions", "url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions", "source": "Python documentation"}],
    },
    "example": {
        "title": "A reusable delivery-total function",
        "type": "code",
        "content": (
            "def delivery_total(price, delivery_fee):\n"
            "    return price + delivery_fee\n\n"
            "assert delivery_total(20, 5) == 25\n"
            "assert delivery_total(0, 5) == 5\n"
            "assert delivery_total(12.5, 2.5) == 15.0\n\n"
            "print(delivery_total(20, 5))  # 25"
        ),
        "explanation": "`price` and `delivery_fee` are parameters. Each call provides arguments, and `return` makes the sum available to `assert` and `print`.",
    },
    "practice": {
        "type": "practical",
        "title": "Write a temperature conversion function",
        "task": "Write `celsius_to_fahrenheit(celsius)` that returns the Fahrenheit value using `(celsius * 9 / 5) + 32`. Do not print inside the function. Include your function and a short note explaining why `return` is needed.",
        "response_type": "code",
        "competency": "Python Functions",
        "starter_code": "def celsius_to_fahrenheit(celsius):\n    # write your code here\n    pass\n",
        "automated_tests": [
            {"input": [0], "expected": 32},
            {"input": [100], "expected": 212},
            {"input": [-40], "expected": -40},
            {"input": [37.5], "expected": 99.5},
        ],
    },
    "mini_check": {
        "questions": [
            {"id": "m1", "type": "mcq", "question": "Which line sends a computed value back to the caller?", "options": ["print(total)", "return total", "def total", "total = input()"], "correct_answer": "return total", "competency": "Python Functions", "difficulty": "beginner", "misconception_hint": "Compare what each construct does after the function call finishes."},
            {"id": "m2", "type": "mcq", "question": "In `def greet(name):`, what is `name`?", "options": ["An argument", "A parameter", "A return value", "A module"], "correct_answer": "A parameter", "competency": "Python Functions", "difficulty": "beginner", "misconception_hint": "Look at whether the name appears in the definition or at a call site."},
            {"id": "m3", "type": "mcq", "question": "What does `delivery_total(20, 5)` evaluate to in the lesson example?", "options": ["20", "5", "25", "It only prints a value"], "correct_answer": "25", "competency": "Python Functions", "difficulty": "beginner", "misconception_hint": "Follow the arithmetic in the function body using both supplied values."},
        ]
    },
    # Display translations deliberately retain canonical English answer values.
    # The client uses these question strings/options only for presentation; the
    # persisted Mini Check continues to grade its immutable canonical set.
    "locales": {
        "ar": {
            "learn": {
                "title": "دوال بايثون",
                "explanation": "الدالة هي وصفة لها اسم لمهمة صغيرة. نستخدم `def` لتعريفها، والمعاملات تستقبل المدخلات، و`return` يرجّع النتيجة للكود الذي استدعى الدالة.",
                "key_ideas": ["عرّف الدالة بـ `def name(parameters):` واكتب جسمها بمسافة بادئة.", "المعامل اسمه داخل تعريف الدالة، أما القيمة التي نمررها عند الاستدعاء فهي argument.", "استخدم `return` عندما يحتاج الكود التالي للنتيجة؛ `print` يعرضها فقط."],
                "key_terms": {"دالة": "كتلة كود لها اسم ويمكن إعادة استخدامها.", "معامل": "اسم داخل تعريف الدالة يستقبل مدخلاً.", "قيمة مُعادة": "قيمة ترسلها الدالة إلى المستدعي."},
                "job_relevance": "الدوال تجعل أجزاء الكود في التطبيقات والتحليل والأتمتة قابلة لإعادة الاستخدام والاختبار.",
                "common_mistake": "لا تخلط بين `print(total)` و`return total`: الأولى تعرض القيمة فقط، والثانية تسمح للكود التالي باستخدامها.",
                "worked_example": "المثال يحسب إجمالي التوصيل من سعر ورسوم، ثم يتحقق من القيمة المعادة بأكثر من مدخل.",
            },
            "example": {"title": "دالة قابلة لإعادة الاستخدام لحساب إجمالي التوصيل", "type": "code", "content": "def delivery_total(price, delivery_fee):\n    return price + delivery_fee\n\nassert delivery_total(20, 5) == 25\nassert delivery_total(0, 5) == 5\nassert delivery_total(12.5, 2.5) == 15.0\n\nprint(delivery_total(20, 5))  # 25", "explanation": "`price` و`delivery_fee` معاملان. كل استدعاء يمرر قيماً، و`return` يجعل المجموع متاحاً لـ `assert` و`print`."},
            "practice": {"title": "اكتب دالة لتحويل الحرارة", "task": "اكتب `celsius_to_fahrenheit(celsius)` لترجع قيمة فهرنهايت باستخدام `(celsius * 9 / 5) + 32`. لا تستخدم `print` داخل الدالة. أضف الدالة وجملة قصيرة تشرح لماذا نستخدم `return`.", "response_type": "code", "competency": "Python Functions", "starter_code": "def celsius_to_fahrenheit(celsius):\n    # اكتب الكود هنا\n    pass\n"},
            "mini_check": {"questions": [
                {"id": "m1", "question": "أي سطر يرسل قيمة محسوبة للكود اللي استدعى الدالة؟", "options": ["print(total)", "return total", "def total", "total = input()"], "misconception_hint": "قارن وظيفة كل تركيب بعد ما ينتهي استدعاء الدالة."},
                {"id": "m2", "question": "في `def greet(name):`، إيه وصف `name`؟", "options": ["قيمة مرّرتها عند الاستدعاء", "معامل في تعريف الدالة", "قيمة راجعة", "وحدة برمجية"], "misconception_hint": "بصّ: الاسم مكتوب في تعريف الدالة ولا وقت استدعائها؟"},
                {"id": "m3", "question": "إيه قيمة `delivery_total(20, 5)` في مثال الدرس؟", "options": ["20", "5", "25", "بتطبع قيمة بس"], "misconception_hint": "اتبع العملية الحسابية جوه جسم الدالة باستخدام القيمتين."},
            ]},
        },
    },
}


PYTHON_ERROR_HANDLING = {
    "status": "complete",
    "skill_aliases": ("python", "python programming"),
    "competency": "Python Error Handling",
    "objective": "Handle an expected conversion error with try/except and return a clear result.",
    "prerequisites": [{
        "competency": "Python Functions",
        "relationship": "required foundation",
        "why": "Handling an error inside a function is easier to follow after you can read parameters and return values.",
    }],
    "roadmap_rationale": "Python Error Handling follows Python Functions because programs need a safe response when real input cannot be converted or processed.",
    "learn": {
        "title": "Python Error Handling",
        "explanation": "An **exception** is Python's signal that an operation cannot continue normally. Put code that may fail in `try`; use `except ValueError` for a value in the wrong format. Handle the specific error you expect, then return a useful result instead of letting the program stop.",
        "key_ideas": ["`try` contains an operation that may raise an exception.", "`except ValueError` handles invalid numeric text; it should not hide unrelated errors.", "Return a value from both the success and error paths so the caller can decide what to do."],
        "key_terms": {"exception": "A runtime problem Python reports.", "try": "The block containing an operation that may fail.", "except": "The block that handles one expected exception."},
        "job_relevance": "Programs receive incomplete and incorrectly formatted input. Specific handling keeps a small failure from crashing the whole task.",
        "common_mistake": "Do not write bare `except:` here: it can hide programming mistakes that should be fixed.",
        "worked_example": "The example turns a text age into an integer. `\"24\"` returns `24`; `\"twenty\"` returns `None` without crashing.",
        "grounding_sources": [{"title": "Python documentation: Errors and Exceptions", "url": "https://docs.python.org/3/tutorial/errors.html", "source": "Python documentation"}],
    },
    "example": {
        "title": "Convert an age safely",
        "type": "code",
        "content": "def parse_age(text):\n    try:\n        return int(text)\n    except ValueError:\n        return None\n\nprint(parse_age(\"24\"))      # 24\nprint(parse_age(\"twenty\"))  # None",
        "explanation": "`int(\"24\")` succeeds, so the function returns `24`. `int(\"twenty\")` raises `ValueError`, so the matching `except` returns `None`. The code is not executed by SkillBridge; these outputs explain Python's expected behavior.",
    },
    "practice": {
        "type": "practical", "title": "Parse a score without crashing",
        "task": "Write `parse_score(text)`. It should return `int(text)` for numeric text such as `\"85\"`. If the text is not an integer such as `\"eighty\"`, catch only `ValueError` and return `None`. Add one sentence explaining why a bare `except:` is not used.",
        "response_type": "code", "competency": "Python Error Handling",
        "starter_code": "def parse_score(text):\n    # convert text safely\n    pass\n",
        "automated_tests": [{"input": ["85"], "expected": 85}, {"input": ["0"], "expected": 0}, {"input": ["eighty"], "expected": None}],
    },
    "mini_check": {"questions": [
        {"id": "e1", "type": "mcq", "question": "Which exception does `int(\"eighty\")` raise?", "options": ["ValueError", "TypeError", "KeyError", "No exception"], "correct_answer": "ValueError", "competency": "Python Error Handling", "difficulty": "beginner", "misconception_hint": "Consider what kind of conversion the expression attempts and why the input cannot satisfy it."},
        {"id": "e2", "type": "mcq", "question": "What does `parse_age(\"twenty\")` return in the worked example?", "options": ["24", "None", "\"twenty\"", "The program must crash"], "correct_answer": "None", "competency": "Python Error Handling", "difficulty": "beginner", "misconception_hint": "Trace the error path in the function after the conversion cannot succeed."},
        {"id": "e3", "type": "mcq", "question": "Why is `except ValueError:` safer than a bare `except:` here?", "options": ["It handles the expected invalid-number input without hiding every other bug", "It runs faster", "It converts all text to integers", "It removes the need for try"], "correct_answer": "It handles the expected invalid-number input without hiding every other bug", "competency": "Python Error Handling", "difficulty": "beginner", "misconception_hint": "Think about which problems should still be visible to the developer."},
    ]},
    # Presentation-only reviewed Arabic fields.  Question answer values remain
    # canonical so a persisted Mini Check is evaluated against exactly the
    # content it was issued with.
    "locales": {
        "ar": {
            "learn": {
                "title": "التعامل مع أخطاء بايثون",
                "explanation": "الاستثناء هو إشارة من بايثون إلى أن العملية لا يمكن أن تستمر بشكل طبيعي. ضع السطر الذي قد يفشل داخل `try`، واستخدم `except ValueError` عندما تكون قيمة النص بصيغة غير صحيحة. تعامل مع الخطأ المتوقع تحديدًا، ثم أعد نتيجة مفيدة بدل أن يتوقف البرنامج.",
                "key_ideas": ["يحتوي `try` على عملية قد تثير استثناءً.", "يتعامل `except ValueError` مع النص الرقمي غير الصحيح من دون إخفاء أخطاء أخرى.", "أعد قيمة في مسار النجاح ومسار الخطأ كي يقرر المستدعي ما يفعله."],
                "key_terms": {"استثناء": "مشكلة وقت تشغيل يبلغ عنها بايثون.", "try": "كتلة تحتوي على عملية قد تفشل.", "except": "كتلة تعالج استثناءً متوقعًا."},
                "job_relevance": "تصل البرامج مدخلات ناقصة أو بصيغة خاطئة؛ التعامل المحدد مع الخطأ يمنع فشلًا صغيرًا من إيقاف المهمة كلها.",
                "common_mistake": "لا تستخدم `except:` بلا اسم هنا؛ فقد يخفي خطأً برمجيًا يجب إصلاحه.",
                "worked_example": "يحوّل المثال نص العمر إلى عدد صحيح. تعيد `\"24\"` القيمة `24`، وتعطي `\"twenty\"` القيمة `None` من دون توقف البرنامج.",
            },
            "example": {
                "title": "تحويل العمر بأمان",
                "type": "code",
                "content": "def parse_age(text):\n    try:\n        return int(text)\n    except ValueError:\n        return None\n\nprint(parse_age(\"24\"))      # 24\nprint(parse_age(\"twenty\"))  # None",
                "explanation": "ينجح `int(\"24\")` فتُعاد `24`. أما `int(\"twenty\")` فيثير `ValueError`، لذلك تعيد كتلة `except` القيمة `None`. هذا المثال للشرح؛ SkillBridge لا ينفذ هذا الكود.",
            },
            "practice": {
                "title": "حلّل درجة من دون توقف البرنامج",
                "task": "اكتب `parse_score(text)`. يجب أن تعيد `int(text)` للنص الرقمي مثل `\"85\"`. إذا لم يكن النص عددًا صحيحًا مثل `\"eighty\"`، التقط `ValueError` فقط وأعد `None`. أضف جملة تشرح لماذا لا نستخدم `except:` بلا اسم.",
                "response_type": "code", "competency": "Python Error Handling",
                "starter_code": "def parse_score(text):\n    # حوّل النص بأمان هنا\n    pass\n",
            },
            "mini_check": {"questions": [
                {"id": "e1", "question": "أي استثناء بينتج من `int(\"eighty\")`؟", "options": ["ValueError", "TypeError", "KeyError", "مفيش استثناء"], "misconception_hint": "فكّر التحويل ده بيحاول يعمل إيه وليه النص المدخل مش مناسب له."},
                {"id": "e2", "question": "إيه اللي بترجعه `parse_age(\"twenty\")` في المثال؟", "options": ["24", "None", "\"twenty\"", "البرنامج لازم يقف بخطأ"], "misconception_hint": "اتبع مسار الخطأ في الدالة بعد ما التحويل ما ينجحش."},
                {"id": "e3", "question": "ليه `except ValueError:` أأمن من `except:` من غير اسم هنا؟", "options": ["بيعالج إدخال الرقم الغلط من غير ما يخفي باقي الأخطاء", "أسرع", "بيحوّل كل النصوص لأرقام", "بيغني عن try"], "misconception_hint": "فكّر في المشاكل اللي المفروض تفضل ظاهرة للمطوّر."},
            ]},
        },
    },
}


# This is deliberately the only complete SQL topic.  The rest of the existing
# SQL blueprint remains useful for diagnostics/planning, but has no canonical
# lesson in this knowledge base and must therefore stay experimental/unverified.
SQL_QUERIES_FILTERING = {
    "status": "complete",
    "skill_aliases": ("sql", "structured query language"),
    "competency": "SQL Queries & Filtering",
    "objective": "Retrieve named columns with SELECT and narrow rows with a precise WHERE condition.",
    "prerequisites": [{
        "competency": "Tables, rows, and columns",
        "relationship": "required foundation",
        "why": "A SELECT query names columns from a table, and a WHERE condition compares values stored in its rows.",
    }],
    "roadmap_rationale": (
        "SQL Queries & Filtering is the first complete SQL topic because reliable data work starts by "
        "requesting only the columns and rows needed. Sorting, aggregation, joins, and all other SQL "
        "topics remain separately scoped and are not represented as completed lessons here."
    ),
    "learn": {
        "title": "SQL Queries & Filtering",
        "explanation": (
            "`SELECT` chooses the columns you want to read, `FROM` names the table, and `WHERE` keeps "
            "only rows that meet a condition. Start with named columns instead of `SELECT *` when you know "
            "what the task needs. A string value is written in single quotes."
        ),
        "key_ideas": [
            "`SELECT name, email` returns only those two columns, in that order.",
            "`FROM customers` identifies the table being queried.",
            "`WHERE city = 'Cairo'` filters rows; it does not change the table.",
            "Use `=` for equality and quote text values; numbers are normally written without quotes.",
        ],
        "key_terms": {
            "query": "An instruction that asks a database for data.",
            "column": "A named field such as `name` or `city` in a table.",
            "row": "One record in a table.",
            "filter": "A condition in `WHERE` that decides which rows are returned.",
        },
        "job_relevance": "Analysts and developers use small, precise queries to inspect the right records without changing source data.",
        "common_mistake": "Do not use `=` without quotes for text such as Cairo, and do not confuse `WHERE` with a command that edits rows.",
        "worked_example": "The example reads each matching customer's name and email from the `customers` table; it does not insert, update, delete, or execute anything in SkillBridge.",
        "depth_note": "Canonical SQL foundation content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": "Examples use standard SELECT/FROM/WHERE syntax. SkillBridge does not provide a SQL database or execute learner queries.",
        "grounding_sources": [
            {"title": "PostgreSQL documentation: Querying a Table", "url": "https://www.postgresql.org/docs/current/tutorial-select.html", "source": "PostgreSQL documentation"},
            {"title": "SQLite documentation: SELECT", "url": "https://sqlite.org/lang_select.html", "source": "SQLite documentation"},
        ],
    },
    "example": {
        "title": "Find Cairo customers",
        "type": "sql",
        "content": "SELECT name, email\nFROM customers\nWHERE city = 'Cairo';",
        "explanation": "This query asks for the `name` and `email` columns only, from rows whose `city` is exactly `Cairo`. It is a worked example, not a query that SkillBridge runs.",
    },
    "practice": {
        "type": "practical",
        "title": "Filter active Cairo customers",
        "task": "Write one read-only SQL query that returns `name` and `email` from `customers` only for rows where `city` is `Cairo` and `status` is `active`. Add one short sentence explaining what each WHERE condition filters.",
        "response_type": "sql",
        "language": "sql",
        "competency": "SQL Queries & Filtering",
        "starter_code": "SELECT name, email\nFROM customers\nWHERE city = 'Cairo'\n  AND status = 'active';",
        "evaluation_note": "SkillBridge performs a static text/structure review only: it checks for a read-only SELECT, the expected table, requested columns, and both filters. It does not connect to a database or execute SQL, so the review cannot prove runtime results.",
    },
    "mini_check": {"questions": [
        {"id": "s1", "type": "mcq", "question": "Which clause narrows a query to rows where `city` is `Cairo`?", "options": ["WHERE city = 'Cairo'", "SELECT city", "FROM Cairo", "ORDER BY city"], "correct_answer": "WHERE city = 'Cairo'", "competency": "SQL Queries & Filtering", "difficulty": "beginner", "misconception_hint": "Choose the clause whose role is deciding which records stay in the result."},
        {"id": "s2", "type": "mcq", "question": "What does `SELECT name, email` request?", "options": ["Only the name and email columns", "Every column in the table", "Only rows with an email", "A new table"], "correct_answer": "Only the name and email columns", "competency": "SQL Queries & Filtering", "difficulty": "beginner", "misconception_hint": "Distinguish a list of requested fields from a condition that filters rows."},
        {"id": "s3", "type": "mcq", "question": "Which query is a read-only request for active Cairo customers?", "options": ["SELECT name, email FROM customers WHERE city = 'Cairo' AND status = 'active';", "DELETE FROM customers WHERE city = 'Cairo';", "UPDATE customers SET status = 'active';", "INSERT INTO customers (city) VALUES ('Cairo');"], "correct_answer": "SELECT name, email FROM customers WHERE city = 'Cairo' AND status = 'active';", "competency": "SQL Queries & Filtering", "difficulty": "beginner", "misconception_hint": "Check whether the statement reads existing records or attempts to change them."},
    ]},
    "locales": {
        "ar": {
            "learn": {
                "title": "استعلامات SQL والتصفية",
                "explanation": "`SELECT` بتحدد الأعمدة اللي عايز تقراها، و`FROM` بتحدد الجدول، و`WHERE` بتحتفظ بالصفوف اللي تحقق شرط. لما تعرف الأعمدة المطلوبة، سمِّيها بدل `SELECT *`. النصوص بتتكتب بين علامتي اقتباس مفردتين.",
                "key_ideas": ["`SELECT name, email` بترجع العمودين دول فقط وبالترتيب ده.", "`FROM customers` بتحدد الجدول اللي بنسأل عنه.", "`WHERE city = 'Cairo'` بتفلتر الصفوف ولا تعدّل الجدول.", "استخدم `=` للمساواة وحط النص بين اقتباس مفرد؛ الأرقام غالباً من غير اقتباس."],
                "key_terms": {"استعلام": "تعليمة بتطلب بيانات من قاعدة البيانات.", "عمود": "حقل له اسم مثل `name` أو `city` داخل جدول.", "صف": "سجل واحد داخل الجدول.", "تصفية": "شرط في `WHERE` يحدد الصفوف الراجعة."},
                "job_relevance": "المحللون والمطورون يستخدمون استعلامات صغيرة ودقيقة لقراءة السجلات المطلوبة من غير تعديل البيانات المصدرية.",
                "common_mistake": "ما تكتبش نص مثل Cairo من غير اقتباس، وما تخلطش بين `WHERE` وبين أمر بيعدّل الصفوف.",
                "worked_example": "المثال بيقرأ الاسم والبريد للعملاء المطابقين من جدول `customers`؛ SkillBridge لا ينفذ الاستعلام ولا يعدّل بيانات.",
                "depth_note": "محتوى تأسيسي ثابت لـ SQL من قاعدة المعرفة المراجَعة، وليس محتوى مولداً حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم صياغة SELECT/FROM/WHERE القياسية. SkillBridge لا يوفر قاعدة بيانات SQL ولا ينفذ استعلامات المتعلم.",
            },
            "example": {"title": "ابحث عن عملاء القاهرة", "type": "sql", "content": "SELECT name, email\nFROM customers\nWHERE city = 'Cairo';", "explanation": "الاستعلام يطلب عمودي `name` و`email` فقط من الصفوف اللي قيمة `city` فيها Cairo. ده مثال للشرح وليس استعلاماً ينفذه SkillBridge."},
            "practice": {"title": "فلتر العملاء النشطين في القاهرة", "task": "اكتب استعلام SQL واحد للقراءة فقط يرجع `name` و`email` من `customers` للصفوف اللي `city` فيها Cairo و`status` فيها active. أضف جملة قصيرة تشرح كل شرط في WHERE بيصفي إيه.", "response_type": "sql", "language": "sql", "competency": "SQL Queries & Filtering", "starter_code": "SELECT name, email\nFROM customers\nWHERE city = 'Cairo'\n  AND status = 'active';", "evaluation_note": "SkillBridge يعمل مراجعة ثابتة للنص والبنية فقط: بيتأكد من SELECT للقراءة، والجدول، والأعمدة، والشرطين. لا يتصل بقاعدة بيانات ولا ينفذ SQL، لذلك المراجعة لا تثبت نتيجة وقت التشغيل."},
            "mini_check": {"questions": [
                {"id": "s1", "question": "أي جزء بيحدد الصفوف اللي `city` فيها Cairo؟", "options": ["WHERE city = 'Cairo'", "SELECT city", "FROM Cairo", "ORDER BY city"], "misconception_hint": "اختار الجزء اللي وظيفته يقرر السجلات اللي تفضل في النتيجة."},
                {"id": "s2", "question": "`SELECT name, email` بيطلب إيه؟", "options": ["عمودي الاسم والبريد بس", "كل أعمدة الجدول", "الصفوف اللي فيها بريد بس", "جدول جديد"], "misconception_hint": "فرّق بين قائمة أعمدة بنطلبها وشرط بيصفي الصفوف."},
                {"id": "s3", "question": "أي استعلام للقراءة بس عن عملاء القاهرة النشطين؟", "options": ["SELECT name, email FROM customers WHERE city = 'Cairo' AND status = 'active';", "DELETE FROM customers WHERE city = 'Cairo';", "UPDATE customers SET status = 'active';", "INSERT INTO customers (city) VALUES ('Cairo');"], "misconception_hint": "شوف الاستعلام بيقرأ سجلات موجودة ولا بيحاول يغيرها."},
            ]},
        },
    },
}


DOCKER_CONTAINERS = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Containers",
    "objective": "Run, inspect, stop, and remove a named container with the modern Docker CLI.",
    "objectives": [
        "Explain what a container is: an isolated running instance of an image.",
        "Start a named background container with `docker run -d --name`.",
        "Check running and stopped containers with `docker ps` and `docker ps -a`, and read output with `docker logs`.",
        "Stop a container with `docker stop`, restart it with `docker start`, and remove it with `docker rm`.",
    ],
    "prerequisites": [],
    "roadmap_rationale": (
        "Containers is the first complete Docker topic because every later Docker topic — images, Dockerfiles, "
        "ports, volumes, networking, Compose — operates on a running container. Starting here means the "
        "learner can always answer 'what is running, and why did it stop?' before building anything."
    ),
    "learn": {
        "title": "Containers",
        "explanation": (
            "A **container** is a running instance of an **image**: an isolated process with its own filesystem, "
            "started by the Docker Engine. `docker run` creates and starts one, `-d` runs it in the background "
            "(detached), and `--name` gives it a stable name every later command can use."
        ),
        "key_ideas": [
            "`docker run -d --name web -p 8080:80 nginx:1.27` starts a background container named `web` from the `nginx:1.27` image and maps host port 8080 to container port 80.",
            "`docker ps` lists running containers; `docker ps -a` also includes stopped ones.",
            "`docker logs web` shows a container's output; `docker inspect web` shows its full configuration.",
            "`docker stop web` stops the container but keeps it (restart with `docker start web`); `docker rm web` removes it and only works once it is stopped (or with `-f`).",
        ],
        "key_terms": {
            "container": "A running, isolated instance of an image managed by the Docker Engine.",
            "image": "The read-only template a container is started from.",
            "detached mode": "Running a container in the background with `-d` instead of tying up your terminal.",
            "container name": "The stable label passed with `--name`, used by logs, stop, start, and rm.",
        },
        "job_relevance": (
            "Deploying, checking, and restarting services in containers is day-to-day work for backend, DevOps, "
            "and data engineers. 'Is it running, and what did it log?' is the first question in almost every "
            "container incident."
        ),
        "real_world_example": (
            "A teammate pings you: 'the staging API stopped responding.' You run `docker ps` — the API container "
            "is not listed, but `docker ps -a` shows it exited 20 minutes ago. You read `docker logs` to find the "
            "crash reason, fix the cause, then `docker start` the same container (or `docker rm` it and run a "
            "fresh one). The container lifecycle is how you answer 'what is running and why did it stop?' in minutes."
        ),
        "common_mistake": "Do not confuse a container with an image: the image is the template, the container is the running instance. Removing the container does not remove the image, and a stopped container still exists until you run `docker rm`.",
        "worked_example": "The example starts one background nginx container, checks it, reads its logs, then stops and removes it.",
        "depth_note": "Canonical beginner content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use the modern unified Docker CLI (Docker Engine 23 and later; `docker run` is the shorthand "
            "for `docker container run`). SkillBridge does not execute Docker commands; the outputs described are "
            "what Docker prints when a command succeeds."
        ),
        "grounding_sources": [
            {"title": "Docker docs: What is a container?", "url": "https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/", "source": "Docker documentation"},
            {"title": "docker container run reference", "url": "https://docs.docker.com/reference/cli/docker/container/run/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Run, check, and stop a container",
        "type": "bash",
        "content": (
            "# 1) start a background container from a pinned image\n"
            "docker run -d --name web -p 8080:80 nginx:1.27\n"
            "\n"
            "# 2) confirm it is running\n"
            "docker ps\n"
            "\n"
            "# 3) read its output\n"
            "docker logs web\n"
            "\n"
            "# 4) stop it (it still exists, stopped)\n"
            "docker stop web\n"
            "\n"
            "# 5) remove it for good\n"
            "docker rm web"
        ),
        "explanation": (
            "Each step is one stage of the container lifecycle: `docker run` creates and starts, `docker ps` "
            "confirms, `docker logs` reads output, `docker stop` stops without deleting, and `docker rm` removes. "
            "This is a worked example for reading — SkillBridge does not run these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Bring a service container back to life",
        "task": (
            "Your team's staging web service runs in a Docker container, and a teammate reports it is down. "
            "Write the concrete Docker commands you would run to: (1) check whether the container is running "
            "or stopped, (2) read its recent logs to find why it stopped, (3) start it again if it is stopped, "
            "and (4) remove it cleanly if you instead need to re-run it fresh from the same image. For each "
            "command, add one line saying what success looks like (what Docker prints, or how you verify the "
            "container is healthy again). Finally, explain in one or two sentences how you would debug the "
            "case where `docker logs` shows the container exits immediately after starting. SkillBridge reviews "
            "your commands as text only — it never executes them."
        ),
        "response_type": "command",
        "competency": "Containers",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for concrete `docker ps` / `docker ps -a`, "
            "`docker logs`, `docker start`, and `docker rm` usage against a named container, plus a stated "
            "verification step for each. It does not run Docker, so the review cannot prove runtime results. "
            "A strong answer names the container, uses the right lifecycle command for each step, states how "
            "each step is verified, and gives a concrete debugging idea for the immediate-exit case (for "
            "example: read the logs' error line, check the container's command, or run it once in the "
            "foreground to see the failure). A weak answer says 'restart Docker' or 'delete and retry' with "
            "no logs check, no container name, and no verification."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "c1", "type": "mcq", "question": "Which command lists containers that have already stopped?", "options": ["docker ps", "docker ps -a", "docker logs", "docker images"], "correct_answer": "docker ps -a", "competency": "Containers", "difficulty": "beginner", "misconception_hint": "One flag widens the default listing to include exited containers."},
            {"id": "c2", "type": "mcq", "question": "What is true right after `docker stop web` finishes?", "options": ["It is deleted from disk immediately", "It still exists and can be started again with `docker start web`", "Its image is removed too", "It restarts automatically"], "correct_answer": "It still exists and can be started again with `docker start web`", "competency": "Containers", "difficulty": "beginner", "misconception_hint": "Stopping and removing are separate steps in the container lifecycle."},
            {"id": "c3", "type": "mcq", "question": "In `docker run -d --name web -p 8080:80 nginx:1.27`, what does `-d` do?", "options": ["Runs the container in the background (detached)", "Deletes the container when it exits", "Publishes port 8080", "Pins the image by digest"], "correct_answer": "Runs the container in the background (detached)", "competency": "Containers", "difficulty": "beginner", "misconception_hint": "The flag changes how the container attaches to your terminal, not its networking."},
        ]
    },
    # Display translations deliberately retain canonical English answer values;
    # the persisted Mini Check continues to grade the immutable canonical set.
    "locales": {
        "ar": {
            "learn": {
                "title": "حاويات Docker",
                "explanation": "**الحاوية** هي نسخة شغالة من **صورة (image)**: عملية معزولة ليها نظام ملفات خاص بيها، بيشغّلها Docker Engine. الأمر `docker run` بيعمل الحاوية ويشغّلها، و`-d` بيخلّيها تشتغل في الخلفية (detached)، و`--name` بيديها اسم ثابت تقدر تستخدمه في كل الأوامر اللي بعد كده.",
                "key_ideas": [
                    "`docker run -d --name web -p 8080:80 nginx:1.27` يشغّل حاوية في الخلفية اسمها `web` من صورة `nginx:1.27` وبيوصّل بورت 8080 على جهازك ببورت 80 جوه الحاوية.",
                    "`docker ps` بيوريك الحاويات اللي شغالة؛ `docker ps -a` بيشمل كمان اللي واقفة.",
                    "`docker logs web` بيوريك اللي الحاوية طبعت؛ `docker inspect web` بيعرض كل إعداداتها.",
                    "`docker stop web` بيوقفها بس مش بيحذفها (ترجع تشتغل بـ `docker start web`)؛ `docker rm web` بيحذفها وبيشتغل بس لما تكون واقفة (أو بـ `-f`).",
                ],
                "key_terms": {"حاوية": "نسخة شغالة معزولة من صورة، بيتحكم فيها Docker Engine.", "صورة": "القالب اللي الحاوية بتبدأ منه.", "detached": "تشغيل الحاوية في الخلفية بـ `-d` بدل ما تفضل ماسكة الترمينال.", "اسم الحاوية": "الاسم الثابت اللي بتحدده بـ `--name`، بتستخدمه مع logs وstop وstart وrm."},
                "job_relevance": "تشغيل الخدمات وفحصها وإعادة تشغيلها في حاويات شغل يومي لمهندسي الـ backend والـ DevOps والداتا — «الحاوية شغالة ولا لأ، وطبعت إيه؟» أول سؤال في أغلب مشاكل الحاويات.",
                "real_world_example": "زميلك بيكتب لك: «الـ API بتاع الـ staging مش بيرد.» تجري `docker ps` — الحاوية مش موجودة في القايمة، بس `docker ps -a` بيقولك انتهت من ٢٠ دقيقة. بتقرا `docker logs` تعرف سبب الوقوف، تصلّح المشكلة، وبعدين يا إما `docker start` لنفس الحاوية يا إما `docker rm` وتشغّل واحدة جديدة. دورة حياة الحاوية هي اللي بتخلّيك تجاوب على «إيه اللي شغال وليه وقف؟» في دقايق.",
                "common_mistake": "ما تخلطش بين الحاوية والصورة: الصورة هي القالب، والحاوية هي النسخة اللي شغالة. حذف الحاوية مش بيحذف الصورة، والحاوية اللي واقفة لسه موجودة لحد ما تعمل `docker rm`.",
                "worked_example": "المثال يشغّل حاوية nginx في الخلفية، بيتأكد منها، بيقرا الـ logs، وبعدين بيوقفها ويحذفها.",
                "depth_note": "محتوى تأسيسي ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم الـ Docker CLI الحديث (Docker Engine 23 وما بعده؛ `docker run` اختصار لـ `docker container run`). SkillBridge ما بينفّذش أوامر Docker؛ المخرجات الموصوفة هي اللي Docker بيطبعها لما الأمر ينجح.",
            },
            "example": {
                "title": "شغّل وافحص ووقّف حاوية",
                "type": "bash",
                "content": "# 1) start a background container from a pinned image\ndocker run -d --name web -p 8080:80 nginx:1.27\n\n# 2) confirm it is running\ndocker ps\n\n# 3) read its output\ndocker logs web\n\n# 4) stop it (it still exists, stopped)\ndocker stop web\n\n# 5) remove it for good\ndocker rm web",
                "explanation": "كل خطوة بتمثل مرحلة في دورة حياة الحاوية: `docker run` ينشئ ويشغّل، `docker ps` يتأكد، `docker logs` يقرا المخرجات، `docker stop` يوقف من غير حذف، و`docker rm` يحذف نهائي. ده مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "رجّع حاوية الخدمة للشغل",
                "task": "خدمة الويب بتاعة فريقكم شغالة في حاوية Docker، وزميلك بلّغ إنها واقفة. اكتب أوامر Docker اللي هتشغّلها عشان: (١) تعرف الحاوية شغالة ولا واقفة، (٢) تقرا الـ logs الأخيرة عشان تعرف ليه وقفت، (٣) تشغّلها تاني لو واقفة، و(٤) تحذفها بنضافة لو قررت تشغّل واحدة جديدة من نفس الصورة. مع كل أمر اكتب سطر يقول النجاح شكله إيه (Docker هيطبع إيه، أو هتتأكد إزاي إن الحاوية رجعت سليمة). وفي الآخر اشرح في سطر أو اتنين هتصلّح إزاي الحالة اللي `docker logs` بيظهر فيها إن الحاوية بتنتهي فورًا بعد ما تشتغل. SkillBridge بيراجع أوامرك كنص بس — مش بينفّذها.",
                "response_type": "command",
                "competency": "Containers",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من استخدام `docker ps` / `docker ps -a` و`docker logs` و`docker start` و`docker rm` مع حاوية باسمها، ومن وجود خطوة تحقق لكل أمر. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتسمّي الحاوية، وتستخدم أمر دورة الحياة الصح لكل خطوة، وتقول إزاي بتتأكد من كل خطوة، وبتفكرة حقيقية لحالة الخروج الفوري (مثلًا: قرا سطر الخطأ في الـ logs، أو شغّلها مرة في الـ foreground تشوف الفشل بعينك). الإجابة الضعيفة بتقول «أعمل ريستارت لـ Docker» أو «امسحها وحاول تاني» من غير قراية logs ولا اسم حاوية ولا أي تحقق.",
            },
            "mini_check": {"questions": [
                {"id": "c1", "question": "أي أمر بيوريك الحاويات اللي وقفت خلاص؟", "options": ["docker ps", "docker ps -a", "docker logs", "docker images"], "misconception_hint": "فيه فلاغ واحد بيوسّع القايمة الافتراضية عشان تشمل الحاويات اللي انتهت."},
                {"id": "c2", "question": "إيه اللي بيحصل بعد ما `docker stop web` يخلص؟", "options": ["بتتحذف من على الديسك فورًا", "لسه موجودة وممكن ترجع تشتغل بـ `docker start web`", "صورتها بتتحذف معاها", "بتشتغل تاني لوحدها"], "misconception_hint": "الإيقاف والحذف خطوتين منفصلتين في دورة حياة الحاوية."},
                {"id": "c3", "question": "في `docker run -d --name web -p 8080:80 nginx:1.27`، `-d` بيعمل إيه؟", "options": ["بيشغّل الحاوية في الخلفية (detached)", "بيحذف الحاوية لما تخلص", "بينشر بورت 8080", "بتثبيت الصورة بالـ digest"], "misconception_hint": "الفلاغ ده بيغيّر إزاي الحاوية بتتوصّل بالترمينال بتاعك، مش الشبكة."},
            ]},
        },
    },
}


DOCKER_IMAGES = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Images",
    "objective": "Pull a version-pinned image, inspect and list local images, retag one, and remove an unused image.",
    "objectives": [
        "Explain what an image is: a read-only, layered template identified by a tag or digest.",
        "Pull an exact version with `docker pull nginx:1.27` instead of an unpinned `:latest`.",
        "List local images with `docker images` and inspect one with `docker image inspect`.",
        "Retag an image with `docker tag` and remove an unused one with `docker rmi`.",
    ],
    "prerequisites": [
        {
            "competency": "Containers",
            "relationship": "required foundation",
            "why": "An image only matters once you can run it: the run/stop lifecycle from Containers is the context for pulling, pinning, and cleaning up images.",
        },
    ],
    "roadmap_rationale": (
        "Images follows Containers because every container is started from an image: you learn to run one "
        "before you learn where it comes from, how it is versioned, and how to keep the local store clean. "
        "Dockerfile, Ports, and Volumes later build on both."
    ),
    "learn": {
        "title": "Images",
        "explanation": (
            "An **image** is the read-only template a container starts from: stacked **layers** identified by a "
            "**tag** such as `nginx:1.27` (or an immutable **digest**). `docker pull` downloads it to your machine "
            "once; containers then start from that local copy."
        ),
        "key_ideas": [
            "`docker pull nginx:1.27` downloads that exact version; a plain `docker pull nginx` means `:latest`, a moving pointer that can change underneath you.",
            "`docker images` lists what is stored locally: repository, tag, image ID, and size.",
            "Layers are shared: pulling `nginx:1.27-bookworm` after `nginx:1.27` reuses the identical layers instead of downloading them again.",
            "`docker tag` adds another name to an image; `docker rmi` removes an image only when no container (running or stopped) still uses it.",
        ],
        "key_terms": {
            "image": "The read-only, layered template containers are started from.",
            "tag": "A mutable label such as `1.27` or `latest` pointing at one image version.",
            "digest": "The immutable `sha256:...` identifier that pins exactly one image.",
            "layer": "A reusable filesystem step shared between images.",
        },
        "job_relevance": (
            "Every deployment review asks 'which exact image version is running?'. Pinning tags (or digests) and "
            "knowing what is stored on a server is daily work for anyone who ships services."
        ),
        "real_world_example": (
            "A security audit flags `nginx:latest` on your server — nobody can say which version that pulled. "
            "You pin instead: `docker pull nginx:1.27`, retag your copy for the company registry with "
            "`docker tag nginx:1.27 myregistry.local:5000/web:1.27`, remove the stale entry with `docker rmi`, "
            "and record the image ID in the deployment ticket. At the next audit you answer with one command: "
            "`docker images`."
        ),
        "common_mistake": "Do not rely on `:latest` in anything that must be reproducible: it is a moving pointer, so the same command can pull a different image next month. Pin a version tag (or a digest) instead.",
        "worked_example": "The example pins a version, verifies what is stored locally, retags it for an internal registry, and removes an old image.",
        "depth_note": "Canonical beginner content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use the modern unified Docker CLI (Docker Engine 23 and later; `docker pull` is the shorthand "
            "for `docker image pull`, and image IDs are content-addressed SHA-256 digests). SkillBridge does not "
            "execute Docker commands or pull anything."
        ),
        "grounding_sources": [
            {"title": "Docker docs: What is an image?", "url": "https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/", "source": "Docker documentation"},
            {"title": "docker image pull reference", "url": "https://docs.docker.com/reference/cli/docker/image/pull/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Pull, verify, retag, and clean up an image",
        "type": "bash",
        "content": (
            "# 1) pull an exact version, not :latest\n"
            "docker pull nginx:1.27\n"
            "\n"
            "# 2) confirm it is stored locally\n"
            "docker images\n"
            "\n"
            "# 3) inspect the pinned image (image ID, layers, env)\n"
            "docker image inspect nginx:1.27\n"
            "\n"
            "# 4) retag it for an internal registry\n"
            "docker tag nginx:1.27 myregistry.local:5000/web:1.27\n"
            "\n"
            "# 5) remove an old image no container uses\n"
            "docker rmi nginx:1.25"
        ),
        "explanation": (
            "`docker pull` downloads the pinned version once; `docker images` proves what is stored locally; "
            "`docker image inspect` shows the image ID and layers; `docker tag` adds a registry name without "
            "copying; `docker rmi` frees an unused image. Worked example for reading — SkillBridge does not run "
            "these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Make a deployment reproducible",
        "task": (
            "Your server currently runs `nginx:latest` and nobody can say which version that is — so the next "
            "deploy is not reproducible. Write the Docker commands you would run to: (1) pull a pinned public "
            "version of the image, (2) verify exactly what is now stored locally, including its identifier, "
            "(3) retag that image for a private registry at `myregistry.local:5000`, and (4) clean up the old "
            "local image safely. For each command, add one line stating what success looks like. Then explain in "
            "one sentence why `:latest` is the wrong choice here and what you would pin instead — a version tag "
            "or a digest, and why. SkillBridge reviews your commands as text only — it never executes them."
        ),
        "response_type": "command",
        "competency": "Images",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for a pinned `docker pull` (an explicit tag or digest, "
            "not `:latest`), `docker images` / `docker image inspect` to verify the local copy, a `docker tag` "
            "naming the private registry, and a `docker rmi` cleanup, plus a stated reason why `:latest` is not "
            "reproducible. It does not run Docker, so the review cannot prove runtime results. A strong answer "
            "pins an exact version, states how each step is verified, and explains the tag-versus-digest "
            "trade-off in one honest sentence. A weak answer pulls `:latest` again, skips verification, or "
            "removes an image a container still uses."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "i1", "type": "mcq", "question": "What does `docker pull nginx` (no tag) actually download?", "options": ["The `nginx:latest` tag — whichever version it points to today", "Every tag in the repository", "Only the smallest layer", "A digest-pinned snapshot"], "correct_answer": "The `nginx:latest` tag — whichever version it points to today", "competency": "Images", "difficulty": "beginner", "misconception_hint": "Ask yourself whether the name identifies one fixed version or a moving pointer."},
            {"id": "i2", "type": "mcq", "question": "Why can `docker rmi nginx:1.27` fail even when the command is typed correctly?", "options": ["A container — even a stopped one — still uses that image", "Images can never be removed", "`rmi` only works on dangling images", "Docker must be stopped first"], "correct_answer": "A container — even a stopped one — still uses that image", "competency": "Images", "difficulty": "beginner", "misconception_hint": "Removal is blocked while anything still references the image."},
            {"id": "i3", "type": "mcq", "question": "Two images stored locally share most of their layers. What does that mean for disk space?", "options": ["The shared layers are stored once, not duplicated per image", "Each image keeps a full private copy", "The layers are compressed twice", "Docker deletes the older image automatically"], "correct_answer": "The shared layers are stored once, not duplicated per image", "competency": "Images", "difficulty": "beginner", "misconception_hint": "Think about how the storage driver reuses identical content."},
        ]
    },
    # Display translations deliberately retain canonical English answer values;
    # the persisted Mini Check continues to grade the immutable canonical set.
    "locales": {
        "ar": {
            "learn": {
                "title": "صُوَر Docker",
                "explanation": "**الصورة (image)** هي القالب اللي الحاوية بتبدأ منه: طبقات (layers) للقراءة بس، ليها **تاج (tag)** زي `nginx:1.27` (أو **digest** ثابت مش بيتغير). `docker pull` بينزّلها على جهازك مرة واحدة، وبعدين الحاويات بتبدأ من النسخة المحلية دي.",
                "key_ideas": [
                    "`docker pull nginx:1.27` بينزّل النسخة دي بالظبط؛ أما `docker pull nginx` من غير تاج فمعناه `:latest` — مؤشر متحرك ممكن يتغير من تحتك.",
                    "`docker images` بيوريك المخزن محليًا: الـ repository والتاج والـ image ID والحجم.",
                    "الطبقات مشتركة: لو نزّلت `nginx:1.27-bookworm` بعد `nginx:1.27`، هتلاقي الطبقات المتطابقة بتتاستخدم تاني بدل ما تتنزّل من الأول.",
                    "`docker tag` بيضيف اسم تاني للصورة؛ `docker rmi` بيحذف الصورة بس لما مفيش حاوية (شغالة أو واقفة) لسه بتستخدمها.",
                ],
                "key_terms": {"صورة": "القالب الطبقي للقراءة بس اللي الحاويات بتبدأ منه.", "تاج (tag)": "علامة قابلة للتغيير زي `1.27` أو `latest` بتشاور على نسخة من الصورة.", "digest": "المعرّف الثابت `sha256:...` اللي بيحدد صورة واحدة بالظبط.", "طبقة (layer)": "خطوة نظام ملفات قابلة لإعادة الاستخدام بتتشاور بين الصور."},
                "job_relevance": "أي مراجعة نشر بتسأل «إيه النسخة بالظبط اللي شغالة؟». تثبيت التاجات (أو الـ digests) ومعرفتك إيه المخزّن على السيرفر شغل يومي لأي حد بيشحن خدمات.",
                "real_world_example": "تدقيق أمني علّم على `nginx:latest` عندكم على السيرفر — ومحدش يعرف يقول النسخة اللي اتنزّلت دي إيه. بتعمل التثبيت بدل كده: `docker pull nginx:1.27`، وبتعمل تاج لنسختك على ريجستري الشركة بـ `docker tag nginx:1.27 myregistry.local:5000/web:1.27`، وبتشيل القديم بـ `docker rmi`، وبتسجّل الـ image ID في تيكت النشر. في التدقيق الجاي بتجاوب بأمر واحد: `docker images`.",
                "common_mistake": "ما تعتمدش على `:latest` في أي حاجة لازم تتكرر بنفس الشكل: ده مؤشر بيتحرك، يعني نفس الأمر ممكن ينزّل صورة مختلفة الشهر الجاي. ثبّت تاج نسخة (أو digest) بدل كده.",
                "worked_example": "المثال بيثبّت نسخة، بيتأكد من المخزن المحلي، بيعمل تاج لريجستري داخلي، وبيحذف صورة قديمة.",
                "depth_note": "محتوى تأسيسي ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم الـ Docker CLI الحديث (Docker Engine 23 وما بعده؛ `docker pull` اختصار لـ `docker image pull`، والـ image IDs عبارة عن digests من نوع SHA-256). SkillBridge ما بينفّذش أوامر Docker وما بينزّلش حاجة.",
            },
            "example": {
                "title": "نزّل واتأكد واعمل تاج ونضّف صورة",
                "type": "bash",
                "content": "# 1) pull an exact version, not :latest\ndocker pull nginx:1.27\n\n# 2) confirm it is stored locally\ndocker images\n\n# 3) inspect the pinned image (image ID, layers, env)\ndocker image inspect nginx:1.27\n\n# 4) retag it for an internal registry\ndocker tag nginx:1.27 myregistry.local:5000/web:1.27\n\n# 5) remove an old image no container uses\ndocker rmi nginx:1.25",
                "explanation": "`docker pull` بينزّل النسخة المثبتة مرة واحدة؛ `docker images` بيثبت المخزن محليًا؛ `docker image inspect` بيوريك الـ image ID والطبقات؛ `docker tag` بيضيف اسم ريجستري من غير نسخ؛ و`docker rmi` بيحرر صورة مش مستخدمة. مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "خلّي النشر قابل للتكرار",
                "task": "السيرفر عندكم شغال بـ `nginx:latest` ومحدش يعرف النسخة دي إيه — يعني النشر الجاي مش قابل للتكرار. اكتب أوامر Docker اللي هتشغّلها عشان: (١) تنزّل نسخة مثبتة من الصورة، (٢) تتأكد بالظبط إيه المخزّن محليًا دلوقتي بمعرّفه، (٣) تعمل تاج للصورة دي على ريجستري خاص عند `myregistry.local:5000`، و(٤) تنضّف الصورة القديمة المحلية بأمان. مع كل أمر اكتب سطر يقول النجاح شكله إيه. وبعدين اشرح في جملة ليه `:latest` اختيار غلط هنا، وهتثبّت إيه بداله — تاج نسخة ولا digest — وليه. SkillBridge بيراجع أوامرك كنص بس — مش بينفّذها.",
                "response_type": "command",
                "competency": "Images",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من `docker pull` بتاج أو digest مثبت (مش `:latest`)، ومن `docker images` / `docker image inspect` للتحقق من النسخة المحلية، ومن `docker tag` بيسمّي الريجستري الخاص، ومن تنظيف بـ `docker rmi`، ومن سبب واضح ليه `:latest` مش قابل للتكرار. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتثبّت نسخة بالظبط، وبتقول إزاي بتتأكد من كل خطوة، وبتشرح الفرق بين التاج والـ digest بجملة صادقة. الإجابة الضعيفة بينزّل `:latest` تاني، أو مبتتحققش من حاجة، أو بتحذف صورة لسه فيه حاوية بتستخدمها.",
            },
            "mini_check": {"questions": [
                {"id": "i1", "question": "`docker pull nginx` (من غير تاج) بينزّل إيه بالظبط؟", "options": ["تاج `nginx:latest` — أي نسخة هو مشاور عليها النهارده", "كل التاجات في المستودع", "أصغر طبقة بس", "نسخة مثبتة بالـ digest"], "misconception_hint": "اسأل نفسك: الاسم ده بيحدد نسخة واحدة ثابتة ولا مؤشر بيتحرك؟"},
                {"id": "i2", "question": "ليه `docker rmi nginx:1.27` ممكن يفشل حتى لو الأمر مكتوب صح؟", "options": ["فيه حاوية — حتى لو واقفة — لسه بتستخدم الصورة دي", "الصور عمرها ما بتتحذف", "`rmi` بيشتغل على الـ dangling بس", "لازم تقفل Docker الأول"], "misconception_hint": "الحذف بيتمنع طالما فيه حاجة لسه بتشاور على الصورة."},
                {"id": "i3", "question": "صورتين مخزنين محليًا بيتشاركوا في أغلب الطبقات. معنى ده إيه للمساحة على الديسك؟", "options": ["الطبقات المشتركة بتتخزن مرة واحدة، مش نسخة لكل صورة", "كل صورة بتحتفظ بنسخة كاملة ليها", "الطبقات بتتنضغط مرتين", "Docker بيحذف الصورة الأقدم تلقائيًا"], "misconception_hint": "فكّر إزاي الـ storage driver بيعيد استخدام المحتوى المتطابق."},
            ]},
        },
    },
}


DOCKER_BASIC_COMMANDS = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Basic commands",
    "objective": "Run the most common Docker CLI commands that inspect and interact with containers and images.",
    "objectives": [
        "Verify the Docker installation with `docker --version` and `docker info`.",
        "Pull and run a one-off container with `docker run --rm`.",
        "List running and stopped containers with `docker ps` and `docker ps -a`.",
        "List local images with `docker images`.",
        "Read container output with `docker logs` and run commands inside a container with `docker exec`.",
        "Clean up stopped containers and unused images with `docker rm` and `docker rmi`.",
    ],
    "prerequisites": [],
    "roadmap_rationale": (
        "Basic commands follows Containers and Images because the learner already knows what a "
        "container and image are; this topic turns those concepts into the everyday CLI actions "
        "every Docker user performs."
    ),
    "learn": {
        "title": "Basic commands",
        "explanation": (
            "The Docker CLI is a single command-line tool. A small set of verbs handles most "
            "day-to-day work: `run`, `ps`, `images`, `logs`, `exec`, `rm`, `rmi`, and `info`. "
            "Flags like `--rm` (delete the container when it exits) and `-it` (interactive + TTY) "
            "change how a command behaves without changing what it does."
        ),
        "key_ideas": [
            "`docker --version` and `docker info` prove Docker is installed and show engine details.",
            "`docker run --rm hello-world` downloads the image if needed, runs the container once, and removes it when it exits.",
            "`docker ps` lists running containers; `docker ps -a` also shows stopped ones. `docker images` lists local images.",
            "`docker logs <container>` prints output; `docker exec -it <container> <command>` runs a command inside a running container.",
            "`docker rm <container>` removes a stopped container; `docker rmi <image>` removes an unused image.",
        ],
        "key_terms": {
            "docker cli": "The unified command-line client for Docker Engine.",
            "--rm": "Flag that automatically deletes a container after it stops.",
            "-it": "Flags that make a container interactive with a terminal (`-i` stdin, `-t` TTY).",
            "exec": "The `docker exec` command that runs a process inside an already-running container.",
        },
        "job_relevance": (
            "Checking versions, running one-off containers, reading logs, opening a shell to debug, "
            "and cleaning up are daily tasks for anyone working with Docker."
        ),
        "real_world_example": (
            "You join a new team and need to confirm the environment before running the project. "
            "`docker --version` and `docker info` confirm Docker is healthy; `docker ps` and "
            "`docker images` show what is already running and stored; `docker run --rm hello-world` "
            "proves you can pull and run. In five commands you have a working baseline."
        ),
        "common_mistake": (
            "`docker run --rm` deletes the container only after it stops — it does not delete the image. "
            "`docker exec` runs a command in a running container; it does not create a new container."
        ),
        "worked_example": (
            "The example verifies Docker, runs a one-off hello-world container, lists containers and "
            "images, reads logs, opens a shell inside a running container, and cleans up."
        ),
        "depth_note": "Canonical beginner content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use the modern unified Docker CLI (Docker Engine 23 and later). SkillBridge "
            "does not execute Docker commands; the outputs described are what Docker prints when a "
            "command succeeds."
        ),
        "grounding_sources": [
            {"title": "Docker CLI reference", "url": "https://docs.docker.com/engine/reference/commandline/docker/", "source": "Docker documentation"},
            {"title": "docker container run reference", "url": "https://docs.docker.com/reference/cli/docker/container/run/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Verify, run, inspect, and clean up",
        "type": "bash",
        "content": (
            "# 1) verify Docker is installed\n"
            "docker --version\n"
            "\n"
            "# 2) run a one-off container that removes itself on exit\n"
            "docker run --rm hello-world\n"
            "\n"
            "# 3) list running and stored containers/images\n"
            "docker ps\n"
            "docker ps -a\n"
            "docker images\n"
            "\n"
            "# 4) read logs and open a shell in a running container named api\n"
            "docker logs api\n"
            "docker exec -it api /bin/sh\n"
            "\n"
            "# 5) clean up a stopped container and an unused image\n"
            "docker rm old\n"
            "docker rmi myapp:0.1"
        ),
        "explanation": (
            "These commands cover the daily lifecycle outside of building images: verify the tool, "
            "run a quick smoke test, inspect what exists, debug a running service, and remove "
            "artifacts that are no longer needed. Worked example for reading — SkillBridge does not "
            "run these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Inspect and clean up a local Docker environment",
        "task": (
            "You have inherited a laptop with Docker already installed. Write the Docker commands "
            "you would run to: (1) confirm Docker is installed and show its version, (2) list all "
            "running containers and all stopped containers, (3) list all local images, (4) run a "
            "one-off `hello-world` container that removes itself when it exits, (5) read the logs "
            "of a running container named `api`, (6) open an interactive shell inside the running "
            "`api` container to inspect a file, and (7) remove a stopped container named `old` and "
            "an unused image `myapp:0.1`. For each command, add one line stating the output you "
            "expect or how you verify it worked. SkillBridge reviews your commands as text only — "
            "it never executes them."
        ),
        "response_type": "command",
        "competency": "Basic commands",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for `docker --version` or `docker info`, "
            "`docker ps` / `docker ps -a`, `docker images`, `docker run --rm hello-world`, "
            "`docker logs api`, `docker exec -it api ...`, `docker rm old`, and `docker rmi myapp:0.1`, "
            "plus a stated verification step for each. It does not run Docker, so the review cannot "
            "prove runtime results. A strong answer names the target container/image and states "
            "what success looks like for every step. A weak answer skips verification, confuses "
            "`exec` with `run`, or omits the cleanup commands."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "b1", "type": "mcq", "question": "Which flag removes a container automatically after it exits?", "options": ["--rm", "-d", "-p", "--name"], "correct_answer": "--rm", "competency": "Basic commands", "difficulty": "beginner", "misconception_hint": "Think about the flag whose whole purpose is cleanup on stop."},
            {"id": "b2", "type": "mcq", "question": "What is the difference between `docker ps` and `docker ps -a`?", "options": ["`ps` lists only running containers; `ps -a` also lists stopped ones", "`ps -a` deletes stopped containers", "`ps` shows images", "There is no difference"], "correct_answer": "`ps` lists only running containers; `ps -a` also lists stopped ones", "competency": "Basic commands", "difficulty": "beginner", "misconception_hint": "The `-a` flag widens the listing to include containers that have exited."},
            {"id": "b3", "type": "mcq", "question": "Which command runs a shell inside an already-running container named `api`?", "options": ["docker exec -it api /bin/sh", "docker run api /bin/sh", "docker start api /bin/sh", "docker logs api /bin/sh"], "correct_answer": "docker exec -it api /bin/sh", "competency": "Basic commands", "difficulty": "beginner", "misconception_hint": "One command is meant for entering a running container; the others create or control containers."},
        ]
    },
    "locales": {
        "ar": {
            "learn": {
                "title": "الأوامر الأساسية في Docker",
                "explanation": "أداة سطر الأوامر Docker CLI هي أداة واحدة. مجموعة صغيرة من الأفعال بتغطي أغلب الشغل اليومي: `run`، `ps`، `images`، `logs`، `exec`، `rm`، `rmi`، و`info`. الفلاغات زي `--rm` (بيحذف الحاوية لما تخلص) و`-it` (تفاعلي + ترمينال) بتغيّر سلوك الأمر من غير ما تغيّر وظيفته.",
                "key_ideas": [
                    "`docker --version` و`docker info` بيثبتوا إن Docker مركّب وبيورو تفاصيل الـ engine.",
                    "`docker run --rm hello-world` بينزّل الصورة لو محتاجة، ويشغّل الحاوية مرة واحدة، ويحذفها لما تخلص.",
                    "`docker ps` بيوريك الحاويات الشغالة؛ `docker ps -a` بيضيف كمان اللي واقفة. `docker images` بيوريك الصور المحلية.",
                    "`docker logs <container>` بيطبع المخرجات؛ `docker exec -it <container> <command>` بيشغّل أمر جوه حاوية شغالة.",
                    "`docker rm <container>` بيحذف حاوية واقفة؛ `docker rmi <image>` بيحذف صورة مش مستخدمة.",
                ],
                "key_terms": {"docker cli": "عميل سطر الأوامر الموحّد لـ Docker Engine.", "--rm": "فلاغ بيحذف الحاوية تلقائيًا بعد ما تخلص.", "-it": "فلاغات بتخلي الحاوية تفاعلية مع ترمينال (`-i` stdin، `-t` TTY).", "exec": "الأمر `docker exec` اللي بيشغّل عملية جوه حاوية شغالة أصلاً."},
                "job_relevance": "التحقق من الإصدارات، تشغيل حاويات مؤقتة، قراية الـ logs، فتح شل للتصحيح، والتنظيف هي مهام يومية لأي حد بيشتغل بـ Docker.",
                "real_world_example": "بتنضم لفريق جديد وعايز تتأكد من البيئة قبل ما تشغّل المشروع. `docker --version` و`docker info` بيثبتوا إن Docker سليم؛ `docker ps` و`docker images` بيوروك إيه اللي شغال ومخزّن؛ `docker run --rm hello-world` بيثبت إنك تقدر تنزّل وتشغّل. في خمس أوامر عندك baseline شغّالة.",
                "common_mistake": "`docker run --rm` بيحذف الحاوية بس بعد ما تخلص — مش بيحذف الصورة. `docker exec` بيشغّل أمر جوه حاوية شغالة؛ مش بيعمل حاوية جديدة.",
                "worked_example": "المثال بيتأكد من Docker، بيشغّل حاوية hello-world مرة واحدة، بيسرد الحاويات والصور، بيقرا الـ logs، بيفتح شل جوه حاوية شغالة، وبينضّف في الآخر.",
                "depth_note": "محتوى تأسيسي ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم الـ Docker CLI الحديث (Docker Engine 23 وما بعده). SkillBridge ما بينفّذش أوامر Docker؛ المخرجات الموصوفة هي اللي Docker بيطبعها لما الأمر ينجح.",
                "grounding_sources": [
                    {"title": "مرجع Docker CLI", "url": "https://docs.docker.com/engine/reference/commandline/docker/", "source": "Docker documentation"},
                    {"title": "مرجع docker container run", "url": "https://docs.docker.com/reference/cli/docker/container/run/", "source": "Docker documentation"},
                ],
            },
            "example": {
                "title": "تحقق وشغّل وافحص ونضّف",
                "type": "bash",
                "content": "# 1) verify Docker is installed\ndocker --version\n\n# 2) run a one-off container that removes itself on exit\ndocker run --rm hello-world\n\n# 3) list running and stored containers/images\ndocker ps\ndocker ps -a\ndocker images\n\n# 4) read logs and open a shell in a running container named api\ndocker logs api\ndocker exec -it api /bin/sh\n\n# 5) clean up a stopped container and an unused image\ndocker rm old\ndocker rmi myapp:0.1",
                "explanation": "الأوامر دي بتغطي دورة الحياة اليومية برّا بناء الصور: تأكد من الأداة، شغّل اختبار سريع، افحص الموجود، صحّح حاوية شغالة، وامسح اللي مش محتاجه. مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "افحص ونضّف بيئة Docker محلية",
                "task": "عندك لابتوب فيه Docker مركّب. اكتب أوامر Docker اللي هتشغّلها عشان: (١) تتأكد إن Docker مركّب وتوري الإصدار، (٢) تسرد كل الحاويات الشغالة واللي واقفة، (٣) تسرد كل الصور المحلية، (٤) تشغّل حاوية `hello-world` مرة واحدة وتحذف نفسها لما تخلص، (٥) تقرا الـ logs بتاعة حاوية `api`، (٦) تفتح شل تفاعلي جوه حاوية `api` عشان تفحص ملف، و(٧) تحذف حاوية واقفة اسمها `old` وصورة مش مستخدمة `myapp:0.1`. مع كل أمر اكتب سطر يقول المخرج المتوقع أو إزاي هتتأكد إنه اشتغل. SkillBridge بيراجع أوامرك كنص بس — مش بينفّذها.",
                "response_type": "command",
                "competency": "Basic commands",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من `docker --version` أو `docker info`، و`docker ps` / `docker ps -a`، و`docker images`، و`docker run --rm hello-world`، و`docker logs api`، و`docker exec -it api ...`، و`docker rm old`، و`docker rmi myapp:0.1`، ومن وجود خطوة تحقق لكل أمر. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتسمّي الحاوية/الصورة المستهدفة وتقول النجاح شكله إيه في كل خطوة. الإجابة الضعيفة بتتخطّى التحقق، أو تخلط بين `exec` و`run`، أو تنسى أوامر التنظيف.",
            },
            "mini_check": {"questions": [
                {"id": "b1", "question": "أي فلاغ بيحذف الحاوية تلقائيًا بعد ما تخلص؟", "options": ["--rm", "-d", "-p", "--name"], "misconception_hint": "فكّر في الفلاغ اللي وظيفته الأساسية التنظيف بعد التوقف."},
                {"id": "b2", "question": "إيه الفرق بين `docker ps` و`docker ps -a`؟", "options": ["`ps` بيوري الحاويات الشغالة بس؛ `ps -a` بيضيف كمان اللي واقفة", "`ps -a` بيحذف الحاويات الوقفة", "`ps` بيوري الصور", "مفيش فرق"], "misconception_hint": "الفلاغ `-a` بيوسّع القايمة عشان تشمل الحاويات اللي خلصت."},
                {"id": "b3", "question": "أي أمر بيشغّل شل جوه حاوية شغالة اسمها `api`؟", "options": ["docker exec -it api /bin/sh", "docker run api /bin/sh", "docker start api /bin/sh", "docker logs api /bin/sh"], "misconception_hint": "أمر واحد مخصوص للدخول لحاوية شغالة؛ الباقي بيعمل أو بيتحكم في حاويات."},
            ]},
        },
    },
}


DOCKER_DOCKERFILE = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Dockerfile",
    "objective": "Write a Dockerfile that builds a small, reproducible image using FROM, COPY, RUN, CMD, and EXPOSE.",
    "objectives": [
        "Explain that a Dockerfile is a recipe that builds an image in ordered layers.",
        "Pin a base image version with FROM instead of using :latest.",
        "Copy source files with COPY and install dependencies with RUN.",
        "Set the default container command with CMD.",
        "Document the intended listening port with EXPOSE.",
    ],
    "prerequisites": [
        {
            "competency": "Images",
            "relationship": "required foundation",
            "why": "A Dockerfile produces an image; you need to understand tags, layers, and image storage before writing a recipe that creates one.",
        },
    ],
    "roadmap_rationale": (
        "Dockerfile follows Images because every Dockerfile builds an image. Knowing how tags, "
        "layers, and local image storage work makes the build process meaningful."
    ),
    "learn": {
        "title": "Dockerfile",
        "explanation": (
            "A Dockerfile is a text recipe that tells Docker how to build an image. Each instruction "
            "creates a layer. `FROM` chooses the starting image, `COPY` adds files from the build "
            "context, `RUN` executes commands during the build, `CMD` sets the default command for "
            "containers started from the image, and `EXPOSE` documents the port the service listens on."
        ),
        "key_ideas": [
            "A Dockerfile builds an image; `docker build -t myapp:1.0 .` tags the result.",
            "`FROM python:3.12-slim` pins a specific base image; avoid `:latest` for reproducible builds.",
            "Order matters for caching: copy dependency files first, install, then copy source code.",
            "`CMD` is the default command when a container starts; it can be overridden at runtime.",
            "`EXPOSE` documents the port but does not publish it — `-p` is still required on `docker run`.",
        ],
        "key_terms": {
            "dockerfile": "A text file containing instructions for building a Docker image.",
            "FROM": "Sets the base image for the build.",
            "COPY": "Copies files from the build context into the image.",
            "RUN": "Executes a command during image build, creating a new layer.",
            "CMD": "Sets the default command for containers started from the image.",
            "EXPOSE": "Documents the port the container service listens on.",
            "build context": "The set of files Docker can see while building, usually the directory containing the Dockerfile.",
        },
        "job_relevance": (
            "Almost every containerized project ships a Dockerfile. Writing one that is small, "
            "cache-friendly, and reproducible is a standard backend and DevOps task."
        ),
        "real_world_example": (
            "Your Python API needs a reproducible deploy image. You write a Dockerfile starting "
            "`FROM python:3.12-slim`, copy `requirements.txt` and run `pip install`, then copy the "
            "source and set `CMD [\"python\", \"app.py\"]`. Now any teammate builds the exact same image "
            "with `docker build -t api:1.0 .`."
        ),
        "common_mistake": (
            "Do not use `:latest` in FROM in production: it makes the build non-reproducible. Also, "
            "EXPOSE does not publish the port by itself; you still need `-p` when running the container."
        ),
        "worked_example": (
            "The example writes a small Python API Dockerfile, builds it with a pinned tag, and runs "
            "a container from the resulting image."
        ),
        "depth_note": "Canonical intermediate content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use Dockerfile syntax compatible with Docker Engine 23+ and BuildKit. SkillBridge "
            "does not execute Docker commands."
        ),
        "grounding_sources": [
            {"title": "Dockerfile reference", "url": "https://docs.docker.com/reference/dockerfile/", "source": "Docker documentation"},
            {"title": "Dockerfile best practices", "url": "https://docs.docker.com/build/building/best-practices/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Build a tiny Python API image",
        "type": "bash",
        "content": (
            "# Dockerfile\n"
            "FROM python:3.12-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt .\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY . .\n"
            "EXPOSE 8000\n"
            "CMD [\"python\", \"app.py\"]\n"
            "\n"
            "# Build and run\n"
            "docker build -t api:1.0 .\n"
            "docker run -d --name api -p 8080:8000 api:1.0"
        ),
        "explanation": (
            "The Dockerfile orders layers for caching: dependencies are installed before the source "
            "is copied, so code-only changes reuse the install layer. `EXPOSE` documents port 8000, "
            "and `-p 8080:8000` actually publishes it. Worked example for reading — SkillBridge does "
            "not run these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Write a Dockerfile for a Node.js service",
        "task": (
            "Write a Dockerfile for a Node.js service and the commands to build and run it. Requirements: "
            "(1) Pin a specific Node version in FROM (not `:latest`), (2) set a working directory, "
            "(3) copy `package.json` and `package-lock.json` first and run `npm install` to leverage "
            "layer caching, (4) copy the rest of the source, (5) set the default command to "
            "`node server.js`, (6) document that the service listens on port 3000. Then write the "
            "commands to build the image tagged `myapi:1.0` and run a container named `myapi` that "
            "maps host port 8080 to container port 3000. Add one sentence explaining why you copy "
            "the package files before the source. SkillBridge reviews your Dockerfile and commands "
            "as text only — it never executes them."
        ),
        "response_type": "configuration",
        "competency": "Dockerfile",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for a pinned FROM, WORKDIR, COPY of package "
            "files before source, RUN npm install, COPY of remaining source, EXPOSE 3000, CMD "
            "node server.js, `docker build -t myapi:1.0 .`, and `docker run -d --name myapi -p 8080:3000 myapi:1.0`, "
            "plus an explanation of layer caching. It does not run Docker, so the review cannot prove "
            "runtime results. A strong answer pins a version, orders COPY for caching, and distinguishes "
            "EXPOSE from `-p`. A weak answer uses `:latest`, copies everything in one step, or omits "
            "the port mapping."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "d1", "type": "mcq", "question": "Which Dockerfile instruction sets the base image?", "options": ["FROM", "COPY", "RUN", "CMD"], "correct_answer": "FROM", "competency": "Dockerfile", "difficulty": "beginner", "misconception_hint": "Every Dockerfile starts by choosing what image to build on top of."},
            {"id": "d2", "type": "mcq", "question": "Why is `COPY requirements.txt .` followed by `RUN pip install` before copying the rest of the source?", "options": ["It lets Docker reuse the installed-dependency layer when only code changes", "It makes the image larger", "It is required by the Dockerfile syntax", "It prevents the container from starting"], "correct_answer": "It lets Docker reuse the installed-dependency layer when only code changes", "competency": "Dockerfile", "difficulty": "intermediate", "misconception_hint": "Think about which layers are invalidated when source files change."},
            {"id": "d3", "type": "mcq", "question": "What does `EXPOSE 3000` do?", "options": ["Documents that the container service listens on port 3000", "Publishes port 3000 to the host automatically", "Forces the container to use port 3000", "Creates a Docker network"], "correct_answer": "Documents that the container service listens on port 3000", "competency": "Dockerfile", "difficulty": "beginner", "misconception_hint": "Publishing to the host requires a runtime flag, not just EXPOSE."},
        ]
    },
    "locales": {
        "ar": {
            "learn": {
                "title": "Dockerfile",
                "explanation": "Dockerfile هو وصفة نصية بتقول لـ Docker إزاي تبني صورة. كل تعليمة بتعمل طبقة. `FROM` بيختار الصورة الأساسية، `COPY` بيضيف ملفات من سياق البناء، `RUN` بينفّذ أوامر أثناء البناء، `CMD` بيحدد الأمر الافتراضي لما الحاوية تبدأ، و`EXPOSE` بيوثّق البورت اللي الخدمة بتسمع عليه.",
                "key_ideas": [
                    "الـ Dockerfile بيبني صورة؛ `docker build -t myapp:1.0 .` بيعمل تاج للنتيجة.",
                    "`FROM python:3.12-slim` بيثبّت صورة أساسية محددة؛ تجنّب `:latest` عشان البناء يتكرر بنفس الشكل.",
                    "الترتيب مهم للكاش: انسخ ملفات الاعتماديات الأول، ثبّتها، وبعدين انسخ الكود.",
                    "`CMD` هو الأمر الافتراضي لما الحاوية تبدأ؛ ممكن يتجاوز وقت التشغيل.",
                    "`EXPOSE` بيوثّق البورت بس مش بينشره — لسه محتاج `-p` في `docker run`.",
                ],
                "key_terms": {"dockerfile": "ملف نصي بيحتوي على تعليمات لبناء صورة Docker.", "FROM": "بيحدد الصورة الأساسية للبناء.", "COPY": "بينسخ ملفات من سياق البناء للصورة.", "RUN": "بينفّذ أمر أثناء بناء الصورة ويعمل طبقة جديدة.", "CMD": "بيحدد الأمر الافتراضي للحاويات اللي بتبدأ من الصورة.", "EXPOSE": "بيوثّق البورت اللي خدمة الحاوية بتسمع عليه.", "build context": "مجموعة الملفات اللي Docker شايفها وقت البناء، عادة المجلد اللي فيه الـ Dockerfile."},
                "job_relevance": "تقريبًا كل مشروع بيستخدم حاويات بيشحن Dockerfile. كتابة Dockerfile صغيرة، صديقة للكاش، وقابلة للتكرار هي مهمة أساسية لـ backend وDevOps.",
                "real_world_example": "الـ API بتاع Python محتاج صورة نشر قابلة للتكرار. بتكتب Dockerfile يبدأ بـ `FROM python:3.12-slim`، بتنسخ `requirements.txt` وتشغّل `pip install`، وبعدين بتنسخ المصدر وتحدد `CMD [\"python\", \"app.py\"]`. دلوقتي أي زميل يقدر يبني نفس الصورة بالظبط بـ `docker build -t api:1.0 .`.",
                "common_mistake": "ما تستخدمش `:latest` في FROM في الإنتاج: ده بيخلي البناء مش قابل للتكرار. كمان EXPOSE مش بينشر البورت لوحده؛ لسه محتاج `-p` وقت تشغيل الحاوية.",
                "worked_example": "المثال بيكتب Dockerfile صغير لـ Python API، يبنيه بتاج مثبت، ويشغّل حاوية من الصورة الناتجة.",
                "depth_note": "محتوى متوسط ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم صيغة Dockerfile متوافقة مع Docker Engine 23+ وBuildKit. SkillBridge ما بينفّذش أوامر Docker.",
                "grounding_sources": [
                    {"title": "مرجع Dockerfile", "url": "https://docs.docker.com/reference/dockerfile/", "source": "Docker documentation"},
                    {"title": "أفضل ممارسات Dockerfile", "url": "https://docs.docker.com/build/building/best-practices/", "source": "Docker documentation"},
                ],
            },
            "example": {
                "title": "ابنِ صورة Python API صغيرة",
                "type": "bash",
                "content": "# Dockerfile\nFROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD [\"python\", \"app.py\"]\n\n# Build and run\ndocker build -t api:1.0 .\ndocker run -d --name api -p 8080:8000 api:1.0",
                "explanation": "الـ Dockerfile بيرتّب الطبقات عشان الكاش: الاعتماديات تتثبّت قبل ما يتنسخ الكود، فلو اتغيّر الكود بس بيُستخدم طبقة التثبيت القديمة. `EXPOSE` بيوثّق بورت 8000، و`-p 8080:8000` هو اللي بينشره فعليًا. مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "اكتب Dockerfile لخدمة Node.js",
                "task": "اكتب Dockerfile لخدمة Node.js والأوامر اللي هتبني وتشغّلها. المتطلبات: (١) ثبّت نسخة Node معينة في FROM (مش `:latest`)، (٢) حدّد working directory، (٣) انسخ `package.json` و`package-lock.json` الأول وشغّل `npm install` عشان تستفيد من كاش الطبقات، (٤) انسخ باقي المصدر، (٥) حدّد الأمر الافتراضي `node server.js`، (٦) وثّق إن الخدمة بتسمع على بورت 3000. وبعدين اكتب الأوامر اللي هتبني الصورة بـ تاج `myapi:1.0` وتشغّل حاوية اسمها `myapi` بتوصيل بورت 8080 على الجهاز ببورت 3000 جوه الحاوية. ضيف جملة واحدة تشرح ليه بنسخ ملفات الباكج قبل المصدر. SkillBridge بيراجع الـ Dockerfile والأوامر كنص بس — مش بينفّذهم.",
                "response_type": "configuration",
                "competency": "Dockerfile",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من FROM مثبت، وWORKDIR، وCOPY لملفات الباكج قبل المصدر، وRUN npm install، وCOPY باقي المصدر، وEXPOSE 3000، وCMD node server.js، و`docker build -t myapi:1.0 .`، و`docker run -d --name myapi -p 8080:3000 myapi:1.0`، وشرح طبقات الكاش. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتثبّت نسخة، وترتّب COPY عشان الكاش، وتميّز بين EXPOSE و`-p`. الإجابة الضعيفة بتستخدم `:latest`، أو بتنسخ كل حاجة في خطوة واحدة، أو بتنسى ربط البورت.",
            },
            "mini_check": {"questions": [
                {"id": "d1", "question": "أي تعليمة في Dockerfile بتحدد الصورة الأساسية؟", "options": ["FROM", "COPY", "RUN", "CMD"], "misconception_hint": "كل Dockerfile بيبدأ باختيار الصورة اللي هيبني فوقها."},
                {"id": "d2", "question": "ليه بنعمل `COPY requirements.txt .` وبعدين `RUN pip install` قبل ما ننسخ باقي المصدر؟", "options": ["عشان Docker تستخدم طبقة تثبيت الاعتماديات تاني لما الكود بس هو اللي يتغير", "عشان الصورة تكبر", "ده مطلوب من صيغة Dockerfile", "عشان الحاوية متبدأش"], "misconception_hint": "فكّر أي الطبقات بتتبطل لما ملفات المصدر تتغير."},
                {"id": "d3", "question": "إيه اللي بيعمله `EXPOSE 3000`؟", "options": ["بيوثّق إن خدمة الحاوية بتسمع على بورت 3000", "بينشر بورت 3000 على الجهاز تلقائيًا", "بيلزم الحاوية تستخدم بورت 3000", "بينشئ شبكة Docker"], "misconception_hint": "النشر على الجهاز بيتطلب فلاغ وقت التشغيل، مش بس EXPOSE."},
            ]},
        },
    },
}


DOCKER_PORTS = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Ports",
    "objective": "Publish a container port to the host, inspect port bindings, and understand the difference between EXPOSE and -p.",
    "objectives": [
        "Explain that container ports are isolated from the host by default.",
        "Publish a port with `docker run -p HOST_PORT:CONTAINER_PORT`.",
        "Inspect bindings with `docker port` and `docker inspect`.",
        "Distinguish `EXPOSE` in a Dockerfile from `-p` on the CLI.",
    ],
    "prerequisites": [
        {
            "competency": "Containers",
            "relationship": "required foundation",
            "why": "Port publishing only makes sense once you can run a container and name it; the run/stop lifecycle is the context for exposing services.",
        },
    ],
    "roadmap_rationale": (
        "Ports follows Containers because publishing is meaningless without a running container. "
        "It bridges the gap between a service running inside a container and a client reaching it "
        "from the host."
    ),
    "learn": {
        "title": "Ports",
        "explanation": (
            "By default, a container's network is isolated. A service listening on port 80 inside "
            "the container is not reachable from your laptop unless you publish the port with "
            "`-p HOST_PORT:CONTAINER_PORT` when running it. `EXPOSE` in a Dockerfile only documents "
            "the intended port; it does not publish it."
        ),
        "key_ideas": [
            "A container port is reachable only from inside the container unless published.",
            "`docker run -d --name web -p 8080:80 nginx:1.27` maps host port 8080 to container port 80.",
            "`docker port web` shows the current bindings; `docker inspect web` shows full network details.",
            "`EXPOSE 80` in a Dockerfile is documentation; `-p 8080:80` at runtime does the actual mapping.",
            "Use host port 0 or ephemeral ports only when you do not care which host port is assigned.",
        ],
        "key_terms": {
            "container port": "The port a process listens on inside the container.",
            "host port": "The port on the machine running Docker that is mapped to a container port.",
            "publish": "To make a container port reachable from outside the container using `-p`.",
            "EXPOSE": "A Dockerfile instruction that documents the intended listening port.",
        },
        "job_relevance": (
            "Every containerized service that receives traffic — APIs, databases, frontends — must "
            "publish its port correctly. Misunderstanding EXPOSE versus -p is one of the most common "
            "reasons a container 'is running but not responding'."
        ),
        "real_world_example": (
            "You run a web container but `curl http://localhost` fails. `docker ps` shows the "
            "container is up, but there is no `0.0.0.0:80->80/tcp` binding because you forgot `-p`. "
            "You stop and rerun with `-p 8080:80`, then `curl http://localhost:8080` returns the page."
        ),
        "common_mistake": (
            "`EXPOSE` does not publish a port. A container can `EXPOSE 80` and still be unreachable "
            "from the host unless you start it with `-p`."
        ),
        "worked_example": (
            "The example starts an nginx container with a published port, verifies the binding, "
            "and shows the difference between EXPOSE and -p."
        ),
        "depth_note": "Canonical intermediate content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use the modern unified Docker CLI (Docker Engine 23 and later). SkillBridge "
            "does not execute Docker commands."
        ),
        "grounding_sources": [
            {"title": "Publishing and exposing ports", "url": "https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/", "source": "Docker documentation"},
            {"title": "docker container run reference", "url": "https://docs.docker.com/reference/cli/docker/container/run/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Publish and verify a web container port",
        "type": "bash",
        "content": (
            "# 1) start nginx and publish host port 8080 to container port 80\n"
            "docker run -d --name web -p 8080:80 nginx:1.27\n"
            "\n"
            "# 2) show the port binding\n"
            "docker port web\n"
            "\n"
            "# 3) inspect the network settings\n"
            "docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}}{{$p}} -> {{(index $conf 0).HostPort}}{{end}}' web\n"
            "\n"
            "# 4) test from the host\n"
            "curl http://localhost:8080"
        ),
        "explanation": (
            "`-p 8080:80` bridges the host and the container. `docker port` confirms the mapping, "
            "and `curl` verifies the service is reachable from the host. Worked example for reading — "
            "SkillBridge does not run these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Expose a containerised API on the correct host port",
        "task": (
            "A container named `api` runs a service that listens on port 3000 inside the container, "
            "but you cannot reach it from your laptop. Write the exact `docker run` command you "
            "should have used to start it so the service is reachable on host port 8080, and show "
            "how to verify the binding with `docker port` and `docker inspect`. Then explain the "
            "difference between `EXPOSE 3000` in the Dockerfile and `-p 8080:3000` on the CLI. "
            "SkillBridge reviews your commands as text only — it never executes them."
        ),
        "response_type": "command",
        "competency": "Ports",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for a `docker run` command that uses "
            "`-p 8080:3000` (or equivalent) with `--name api`, `docker port api`, `docker inspect` "
            "to read the binding, and an explanation that EXPOSE documents the port while `-p` "
            "publishes it to the host. It does not run Docker, so the review cannot prove runtime "
            "results. A strong answer names the image, states the exact mapping, and gives a concrete "
            "verify step. A weak answer suggests EXPOSE alone is enough, uses the ports in reverse "
            "order, or omits verification."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "p1", "type": "mcq", "question": "Which `docker run` flag publishes a container port to the host?", "options": ["-p", "-d", "--name", "--rm"], "correct_answer": "-p", "competency": "Ports", "difficulty": "beginner", "misconception_hint": "Look for the flag that creates the host-to-container port mapping."},
            {"id": "p2", "type": "mcq", "question": "What does `EXPOSE 3000` in a Dockerfile do?", "options": ["Documents that the service listens on port 3000", "Publishes port 3000 to the host", "Forwards port 3000 automatically", "Creates a network bridge"], "correct_answer": "Documents that the service listens on port 3000", "competency": "Ports", "difficulty": "beginner", "misconception_hint": "Publishing requires a runtime flag, not just a Dockerfile instruction."},
            {"id": "p3", "type": "mcq", "question": "In `docker run -p 8080:80`, which port belongs to the host?", "options": ["8080", "80", "Both", "Neither"], "correct_answer": "8080", "competency": "Ports", "difficulty": "beginner", "misconception_hint": "The host port is written first in HOST:CONTAINER notation."},
        ]
    },
    "locales": {
        "ar": {
            "learn": {
                "title": "البورتات في Docker",
                "explanation": "افتراضيًا، شبكة الحاوية معزولة. خدمة بتسمع على بورت 80 جوه الحاوية مش هتوصل من لابتوبك إلا لو نشرت البورت بـ `-p HOST_PORT:CONTAINER_PORT` وقت التشغيل. `EXPOSE` في Dockerfile بيوثّق البورت المقصود بس مش بينشره.",
                "key_ideas": [
                    "بورت الحاوية بيوصل من جوه الحاوية بس إلا لو اتنشر.",
                    "`docker run -d --name web -p 8080:80 nginx:1.27` بيوصّل بورت 8080 على الجهاز ببورت 80 جوه الحاوية.",
                    "`docker port web` بيوري الربط الحالي؛ `docker inspect web` بيوري تفاصيل الشبكة كاملة.",
                    "`EXPOSE 80` في Dockerfile مجرد توثيق؛ `-p 8080:80` وقت التشغيل هو اللي بيعمل الربط الفعلي.",
                    "استخدم بورت 0 على الـ host أو بورتات مؤقتة بس لما يبقى مش مهم أي بورت على الجهاز هيُخصص.",
                ],
                "key_terms": {"container port": "البورت اللي العملية بتسمع عليه جوه الحاوية.", "host port": "البورت على الجهاز اللي Docker شغال عليه واللي بيرتبط ببورت الحاوية.", "publish": "إتاحة بورت الحاوية من برّا باستخدام `-p`.", "EXPOSE": "تعليمة في Dockerfile بتوثّق البورت المقصود."},
                "job_relevance": "كل خدمة في حاوية بتستقبل ترافيك — APIs، قواعد بيانات، frontends — لازم تنشر بورتها صح. عدم الفهم الفرق بين EXPOSE و -p من أشهر أسباب إن الحاوية «شغالة بس مش بترد».",
                "real_world_example": "بتشغّل حاوية ويب بس `curl http://localhost` بيفشل. `docker ps` بيوريك إنها شغالة، بس مفيش ربط `0.0.0.0:80->80/tcp` عشان نسيت `-p`. بتوقفها وتشغّلها تاني بـ `-p 8080:80`، وبعدين `curl http://localhost:8080` بيرجّع الصفحة.",
                "common_mistake": "`EXPOSE` مش بينشر البورت. الحاوية ممكن تكون عاملة `EXPOSE 80` وماتبقاش قابلة للوصول من الجهاز إلا لو تشغّلت بـ `-p`.",
                "worked_example": "المثال بيشغّل حاوية nginx بنشر بورت، بيتأكد من الربط، وبيوري الفرق بين EXPOSE و -p.",
                "depth_note": "محتوى متوسط ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم الـ Docker CLI الحديث (Docker Engine 23 وما بعده). SkillBridge ما بينفّذش أوامر Docker.",
                "grounding_sources": [
                    {"title": "نشر وإتاحة البورتات", "url": "https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/", "source": "Docker documentation"},
                    {"title": "مرجع docker container run", "url": "https://docs.docker.com/reference/cli/docker/container/run/", "source": "Docker documentation"},
                ],
            },
            "example": {
                "title": "انشر بورت حاوية ويب وتأكد منه",
                "type": "bash",
                "content": "# 1) start nginx and publish host port 8080 to container port 80\ndocker run -d --name web -p 8080:80 nginx:1.27\n\n# 2) show the port binding\ndocker port web\n\n# 3) inspect the network settings\ndocker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}}{{$p}} -> {{(index $conf 0).HostPort}}{{end}}' web\n\n# 4) test from the host\ncurl http://localhost:8080",
                "explanation": "`-p 8080:80` بيوصل الجهاز بالحاوية. `docker port` بيثبت الربط، و`curl` بيثبت إن الخدمة قابلة للوصول من الجهاز. مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "أتاح API في الحاوية على البورت الصح",
                "task": "حاوية اسمها `api` شغالة بخدمة بتسمع على بورت 3000 جوهها، بس مش قادرة توصلها من لابتوبك. اكتب أمر `docker run` المظبوط اللي كان المفروض تشغّل بيه الحاوية عشان الخدمة تكون قابلة للوصول على بورت 8080 على الجهاز، وورّي إزاي تتأكد من الربط بـ `docker port` و`docker inspect`. وبعدين اشرح الفرق بين `EXPOSE 3000` في Dockerfile و`-p 8080:3000` في سطر الأوامر. SkillBridge بيراجع أوامرك كنص بس — مش بينفّذها.",
                "response_type": "command",
                "competency": "Ports",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من أمر `docker run` بيستخدم `-p 8080:3000` (أو ما يعادله) مع `--name api`، و`docker port api`، و`docker inspect` لقراية الربط، وشرح إن EXPOSE بيوثّق البورت بينما `-p` بينشره على الجهاز. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتسمّي الصورة، وتحدد الربط بالظبط، وتعطي خطوة تحقق عملية. الإجابة الضعيفة بتقول إن EXPOSE كفاية لوحده، أو تستخدم البورتات بترتيب عكسي، أو تتخطّى التحقق.",
            },
            "mini_check": {"questions": [
                {"id": "p1", "question": "أي فلاغ في `docker run` بينشر بورت الحاوية على الجهاز؟", "options": ["-p", "-d", "--name", "--rm"], "misconception_hint": "دور على الفلاغ اللي بيعمل ربط من بورت الجهاز لبورت الحاوية."},
                {"id": "p2", "question": "إيه اللي بيعمله `EXPOSE 3000` في Dockerfile؟", "options": ["بيوثّق إن الخدمة بتسمع على بورت 3000", "بينشر بورت 3000 على الجهاز", "بيفوّر البورت تلقائيًا", "بينشئ شبكة Docker"], "misconception_hint": "النشر على الجهاز بيتطلب فلاغ وقت التشغيل، مش بس تعليمة في Dockerfile."},
                {"id": "p3", "question": "في `docker run -p 8080:80`، أي بورت تبع الجهاز؟", "options": ["8080", "80", "الاتنين", "ولا واحد"], "misconception_hint": "بورت الجهاز هو اللي بيكتب الأول في صيغة HOST:CONTAINER."},
            ]},
        },
    },
}


DOCKER_VOLUMES = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Volumes",
    "objective": "Use Docker volumes to persist data beyond the container lifecycle and share data between containers.",
    "objectives": [
        "Explain that files written inside a container's writable layer are lost when the container is removed.",
        "Create a named volume with `docker volume create`.",
        "Mount a volume into a container with `docker run -v NAME:PATH`.",
        "List and inspect volumes with `docker volume ls` and `docker volume inspect`.",
        "Choose when to use a named volume versus a bind mount.",
    ],
    "prerequisites": [],
    "roadmap_rationale": (
        "Volumes follows Containers because persistence only matters once you can create and remove "
        "containers. It prepares the learner for stateful services and multi-container Compose stacks."
    ),
    "learn": {
        "title": "Volumes",
        "explanation": (
            "By default, files written inside a container live only as long as the container. A "
            "**Docker volume** is a managed storage area outside the container filesystem. Data in a "
            "volume survives `docker rm`, can be mounted into a replacement container, and can even be "
            "shared by multiple containers at the same time."
        ),
        "key_ideas": [
            "A container's writable layer is deleted when the container is removed; a volume is not.",
            "`docker volume create mydata` creates a named volume managed by Docker.",
            "`docker run -v mydata:/app/data ...` mounts the volume at `/app/data` inside the container.",
            "`docker volume ls` lists volumes; `docker volume inspect mydata` shows where it is mounted and which driver it uses.",
            "Named volumes are easier to back up and move than bind mounts; bind mounts tie a host path directly to a container path.",
        ],
        "key_terms": {
            "volume": "Managed storage outside a container's filesystem that survives container removal.",
            "named volume": "A volume created explicitly with a name, such as `mydata`, so it can be reused.",
            "bind mount": "A mount that maps a specific host path into a container path.",
            "mount point": "The path inside the container where external storage appears.",
            "persistent storage": "Storage that keeps its data after the process or container using it stops.",
        },
        "job_relevance": (
            "Databases, caches, user uploads, and log files must outlive the container. Volumes are the "
            "standard way to keep that data safe across deploys, restarts, and container replacements."
        ),
        "real_world_example": (
            "You upgrade Postgres from 15 to 16. The old container is removed with `docker rm`, but its "
            "data directory was stored in a named volume called `pgdata`. You start the new Postgres "
            "container with the same `-v pgdata:/var/lib/postgresql/data` flag, and the database comes "
            "back online with all tables and rows intact."
        ),
        "common_mistake": (
            "Do not store important data only in the container's writable layer: it is deleted when the "
            "container is removed. Use a volume (or bind mount) for anything that must survive."
        ),
        "worked_example": (
            "The example creates a named volume, runs a container that writes a file into it, removes "
            "the container, and proves the data still exists by mounting the same volume in a new container."
        ),
        "depth_note": "Canonical intermediate content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use the modern unified Docker CLI (Docker Engine 23 and later). SkillBridge does not "
            "execute Docker commands."
        ),
        "grounding_sources": [
            {"title": "Docker volumes", "url": "https://docs.docker.com/engine/storage/volumes/", "source": "Docker documentation"},
            {"title": "Docker storage overview", "url": "https://docs.docker.com/engine/storage/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Persist data with a named volume",
        "type": "bash",
        "content": (
            "# 1) create a named volume\n"
            "docker volume create mydata\n"
            "\n"
            "# 2) run a container that writes to the volume\n"
            "docker run -d --name writer -v mydata:/app/data busybox:1.36 \"\n"
            "  sh -c 'echo hello > /app/data/file.txt'\n"
            "\n"
            "# 3) remove the writer container\n"
            "docker rm writer\n"
            "\n"
            "# 4) run a new container with the same volume and read the file\n"
            "docker run --rm -v mydata:/app/data busybox:1.36 cat /app/data/file.txt"
        ),
        "explanation": (
            "The volume outlives the first container. Even after `docker rm writer`, the file written to "
            "`/app/data` remains in `mydata` and is visible to the second container. Worked example for "
            "reading — SkillBridge does not run these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Keep a database alive across container restarts",
        "task": (
            "Your Postgres container must keep its data even if the container is removed. Write the "
            "Docker commands to: (1) create a named volume called `pgdata`, (2) run a Postgres 16 "
            "container named `db` with the volume mounted at `/var/lib/postgresql/data` and a password "
            "set via `-e POSTGRES_PASSWORD=secret`, (3) confirm the volume is listed and the container "
            "is running, (4) remove the `db` container, and (5) start a new Postgres 16 container named "
            "`db2` using the same volume and show that the previous data is still there. For each step, "
            "add one line stating what output proves it worked. SkillBridge reviews your commands as text "
            "only — it never executes them."
        ),
        "response_type": "command",
        "competency": "Volumes",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for `docker volume create pgdata`, a `docker run` "
            "command with `-v pgdata:/var/lib/postgresql/data` and `-e POSTGRES_PASSWORD=secret`, "
            "`docker volume ls` / `docker volume inspect pgdata` or `docker ps` for verification, "
            "`docker rm db`, and a second `docker run` reusing the same volume. It does not run Docker, "
            "so the review cannot prove runtime results. A strong answer names the volume and container, "
            "states the verification output for every step, and explains why the data survives. A weak "
            "answer omits the volume, forgets the environment variable, or skips verification."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "v1", "type": "mcq", "question": "What happens to data written in a container's writable layer when the container is removed?", "options": ["It is deleted", "It is copied into the image", "It moves to a volume automatically", "It stays forever"], "correct_answer": "It is deleted", "competency": "Volumes", "difficulty": "beginner", "misconception_hint": "The writable layer is part of the container, not a separate persistent store."},
            {"id": "v2", "type": "mcq", "question": "Which command creates a named Docker volume?", "options": ["docker volume create mydata", "docker create volume mydata", "docker run -v mydata", "docker build -v mydata"], "correct_answer": "docker volume create mydata", "competency": "Volumes", "difficulty": "beginner", "misconception_hint": "The noun comes before the verb in the Docker CLI for this resource."},
            {"id": "v3", "type": "mcq", "question": "Which flag mounts a named volume `mydata` into a container at `/app/data`?", "options": ["-v mydata:/app/data", "-p mydata:/app/data", "--name mydata:/app/data", "--rm mydata:/app/data"], "correct_answer": "-v mydata:/app/data", "competency": "Volumes", "difficulty": "beginner", "misconception_hint": "The flag for mounting storage is the same one used for bind mounts."},
        ]
    },
    "locales": {
        "ar": {
            "learn": {
                "title": "الـ Volumes في Docker",
                "explanation": "افتراضيًا، الملفات اللي بتتكتب جوه الحاوية بتعيش لحد ما الحاوية تتشال. الـ **Docker volume** هي مساحة تخزين مُدارة برّا نظام ملفات الحاوية. البيانات في الـ volume بتفوق `docker rm`، وممكن تركّبها في حاوية بديلة، وممكن كمان تشاركها حاويات متعددة في نفس الوقت.",
                "key_ideas": [
                    "طبقة الكتابة في الحاوية بتمسح لما الحاوية تتشال؛ الـ volume لأ.",
                    "`docker volume create mydata` بيعمل volume مسمّى بيديره Docker.",
                    "`docker run -v mydata:/app/data ...` بيركّب الـ volume على مسار `/app/data` جوه الحاوية.",
                    "`docker volume ls` بيسرد الـ volumes؛ `docker volume inspect mydata` بيوري فين متركّب والـ driver المستخدم.",
                    "الـ named volumes أسهل في الـ backup والنقل من الـ bind mounts؛ الـ bind mounts بيربطوا مسار محدد على الـ host مباشرة بالحاوية.",
                ],
                "key_terms": {"volume": "تخزين مُدارة برّا نظام ملفات الحاوية وبيفوق إزالتها.", "named volume": "volume اتعمل باسم صريح زي `mydata` عشان يت reused.", "bind mount": "تركيب بيربط مسار محدد على الـ host بمسار جوه الحاوية.", "mount point": "المسار جوه الحاوية اللي بيظهر فيه التخزين الخارجي.", "persistent storage": "تخزين بيحتفظ بالبيانات بعد ما العملية أو الحاوية توقف."},
                "job_relevance": "قواعد البيانات والـ caches وملفات المستخدمين والـ logs لازم تفوق الحاوية. الـ Volumes هي الطريقة القياسية للحفاظ على البيانات أثناء النشر وإعادة التشغيل واستبدال الحاويات.",
                "real_world_example": "بتعمل upgrade لـ Postgres من 15 لـ 16. الحاوية القديمة اتشالت بـ `docker rm`، بس مجلد البيانات كان في volume اسمه `pgdata`. بتشغّل حاوية Postgres 16 جديدة بنفس الفلاغ `-v pgdata:/var/lib/postgresql/data`، وقاعدة البيانات ترجع شغالة بكل الجداول والصفوف زي ما هي.",
                "common_mistake": "ما تخزّنش بيانات مهمة في طبقة الكتابة بتاعة الحاوية بس: هتمسح لما الحاوية تتشال. استخدم volume (أو bind mount) لأي حاجة لازم تفوق.",
                "worked_example": "المثال بيعمل volume مسمّى، بيشغّل حاوية تكتب ملف فيه، بيمسح الحاوية، وبيثبت إن البيانات لسه موجودة بتركيب نفس الـ volume في حاوية جديدة.",
                "depth_note": "محتوى متوسط ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم الـ Docker CLI الحديث (Docker Engine 23 وما بعده). SkillBridge ما بينفّذش أوامر Docker.",
                "grounding_sources": [
                    {"title": "Docker volumes", "url": "https://docs.docker.com/engine/storage/volumes/", "source": "Docker documentation"},
                    {"title": "نظرة عامة على تخزين Docker", "url": "https://docs.docker.com/engine/storage/", "source": "Docker documentation"},
                ],
            },
            "example": {
                "title": "حافظ على البيانات بـ named volume",
                "type": "bash",
                "content": "# 1) create a named volume\ndocker volume create mydata\n\n# 2) run a container that writes to the volume\ndocker run -d --name writer -v mydata:/app/data busybox:1.36 \\\n  sh -c 'echo hello > /app/data/file.txt'\n\n# 3) remove the writer container\ndocker rm writer\n\n# 4) run a new container with the same volume and read the file\ndocker run --rm -v mydata:/app/data busybox:1.36 cat /app/data/file.txt",
                "explanation": "الـ volume بيفوق الحاوية الأولى. حتى بعد `docker rm writer`، الملف اللي اتكتب في `/app/data` لسه موجود في `mydata` وظاهر للحاوية التانية. مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "أبقِ قاعدة البيانات شغالة بعد استبدال الحاوية",
                "task": "حاوية Postgres عندك لازم تحتفظ ببياناتها حتى لو اتشالت. اكتب أوامر Docker عشان: (١) تعمل volume مسمّى `pgdata`، (٢) تشغّل حاوية Postgres 16 اسمها `db` مركّبة الـ volume على `/var/lib/postgresql/data` وكلمة سر محددة بـ `-e POSTGRES_PASSWORD=secret`، (٣) تتأكد إن الـ volume موجود والحاوية شغالة، (٤) تمسح الحاوية `db`، و(٥) تشغّل حاوية Postgres 16 جديدة اسمها `db2` بنفس الـ volume وتوري إن البيانات القديمة لسه موجودة. لكل خطوة ضيف سطر بيقول إيه المخرج اللي بيثبت نجاحها. SkillBridge بيراجع أوامرك كنص بس — مش بينفّذها.",
                "response_type": "command",
                "competency": "Volumes",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من `docker volume create pgdata`، وأمر `docker run` بيستخدم `-v pgdata:/var/lib/postgresql/data` و`-e POSTGRES_PASSWORD=secret`، و`docker volume ls` / `docker volume inspect pgdata` أو `docker ps` للتحقق، و`docker rm db`، وأمر `docker run` تاني بيستخدم نفس الـ volume. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتسمّي الـ volume والحاوية، وبتقول مخرج التحقق في كل خطوة، وبتشرح ليه البيانات بتفوق. الإجابة الضعيفة بتنسى الـ volume، أو متسيب variable الباسورد، أو تتخطّى التحقق.",
            },
            "mini_check": {"questions": [
                {"id": "v1", "question": "إيه اللي بيحصل للبيانات اللي اتكتبت في طبقة الكتابة بتاعة الحاوية لما الحاوية تتشال؟", "options": ["بتمسح", "بتتنسخ للصورة", "بتروح لـ volume تلقائيًا", "بتفضل للأبد"], "misconception_hint": "طبقة الكتابة جزء من الحاوية، مش تخزين منفصل دائم."},
                {"id": "v2", "question": "أي أمر بيعمل Docker volume مسمّى؟", "options": ["docker volume create mydata", "docker create volume mydata", "docker run -v mydata", "docker build -v mydata"], "misconception_hint": "في الـ Docker CLI الاسم بيجي بعد الفعل بالنسبة للـ resource ده."},
                {"id": "v3", "question": "أي فلاغ بيركّب volume اسمه `mydata` جوه الحاوية على `/app/data`؟", "options": ["-v mydata:/app/data", "-p mydata:/app/data", "--name mydata:/app/data", "--rm mydata:/app/data"], "misconception_hint": "نفس الفلاغ بيستخدم للـ bind mounts كمان."},
            ]},
        },
    },
}


DOCKER_NETWORKING = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Networking",
    "objective": "Connect containers with a user-defined bridge network and use container names as hostnames for service-to-service communication.",
    "objectives": [
        "Explain the difference between the default bridge and a user-defined bridge network.",
        "Create a network with `docker network create`.",
        "Run containers on the same network with `--network`.",
        "Use container names as DNS hostnames to reach another container.",
        "Inspect a network with `docker network inspect`.",
    ],
    "prerequisites": [],
    "roadmap_rationale": (
        "Networking follows Ports because once a learner can publish a single container's port, the next "
        "step is making multiple containers talk to each other reliably by name. It is a prerequisite for Compose."
    ),
    "learn": {
        "title": "Networking",
        "explanation": (
            "By default, every container gets its own network namespace. Containers on the default bridge "
            "can reach each other only by IP address, which changes. A **user-defined bridge network** gives "
            "containers DNS-based names and controlled isolation: containers on the same network can talk by "
            "name, while unrelated containers stay separated."
        ),
        "key_ideas": [
            "The default bridge network does not provide DNS; containers are reached by IP, which is fragile.",
            "`docker network create appnet` creates a user-defined bridge network.",
            "`docker run --network appnet --name web ...` joins a container to that network.",
            "Containers on the same user-defined network can resolve each other by name, e.g. `web` or `db:5432`.",
            "`docker network inspect appnet` shows which containers are attached and their IP addresses.",
        ],
        "key_terms": {
            "network namespace": "An isolated network stack (interfaces, routes, firewall rules) for a container.",
            "bridge network": "A virtual switch inside Docker that connects containers on the same host.",
            "user-defined network": "A custom bridge network created by the user, with built-in DNS and better isolation.",
            "DNS resolution": "Looking up a container by its name to find its IP address.",
            "service discovery": "Finding another service by name rather than by a changing IP address.",
        },
        "job_relevance": (
            "Multi-service applications (web + database + cache) need reliable communication. User-defined "
            "networks are the standard way to give containers stable names and isolate application stacks."
        ),
        "real_world_example": (
            "An API container needs to reach a Postgres container. If they share a user-defined network called "
            "`appnet`, the API can connect to `postgres://db:5432/mydb`. When the Postgres container restarts "
            "and gets a new IP, the name still resolves correctly."
        ),
        "common_mistake": (
            "Do not rely on the default bridge for service-to-service communication: IP addresses change and "
            "there is no DNS. Create a user-defined network and use container names as hostnames."
        ),
        "worked_example": (
            "The example creates a network, runs a database and a web container on it, and shows how the web "
            "container reaches the database by name instead of by IP."
        ),
        "depth_note": "Canonical intermediate content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use the modern unified Docker CLI (Docker Engine 23 and later). SkillBridge does not "
            "execute Docker commands."
        ),
        "grounding_sources": [
            {"title": "Docker networking overview", "url": "https://docs.docker.com/engine/network/", "source": "Docker documentation"},
            {"title": "Bridge network overview", "url": "https://docs.docker.com/engine/network/drivers/bridge/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Connect a web app and a database on the same network",
        "type": "bash",
        "content": (
            "# 1) create a user-defined bridge network\n"
            "docker network create appnet\n"
            "\n"
            "# 2) run a database container on the network\n"
            "docker run -d --name db --network appnet -e POSTGRES_PASSWORD=secret postgres:16\n"
            "\n"
            "# 3) run a web container on the same network, publishing its port\n"
            "docker run -d --name web --network appnet -p 8080:80 myweb:1.0\n"
            "\n"
            "# 4) inspect the network to see attached containers\n"
            "docker network inspect appnet\n"
            "\n"
            "# Inside the web container, the database is reachable at db:5432"
        ),
        "explanation": (
            "Both containers are on `appnet`, so they can resolve each other by name. The web container does "
            "not need to know the database's IP; it uses `db:5432`. Publishing `-p 8080:80` only exposes the "
            "web service to the host. Worked example for reading — SkillBridge does not run these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Wire a web container to a database by name",
        "task": (
            "You need an API container (`api`) to reach a Postgres database container (`db`) without hardcoding "
            "an IP address. Write the commands to: (1) create a user-defined bridge network called `appnet`, "
            "(2) run the `db` container on `appnet` with a password set via environment variable, (3) run the "
            "`api` container on `appnet` publishing host port 8080 to container port 3000, and (4) show how the "
            "API would connect to the database using the container name. Also write the `docker network inspect` "
            "command you would use to verify both containers are attached. SkillBridge reviews your commands as "
            "text only — it never executes them."
        ),
        "response_type": "command",
        "competency": "Networking",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for `docker network create appnet`, two `docker run` "
            "commands using `--network appnet` with `--name db` and `--name api`, `-e POSTGRES_PASSWORD=...`, "
            "`-p 8080:3000`, a connection string or hostname using `db` (not an IP), and `docker network inspect appnet`. "
            "It does not run Docker, so the review cannot prove runtime results. A strong answer explains why a "
            "user-defined network is better than the default bridge for name resolution. A weak answer uses IP "
            "addresses, omits `--network`, or confuses port publishing with internal container DNS."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "n1", "type": "mcq", "question": "What is the main advantage of a user-defined bridge network over the default bridge?", "options": ["Containers can resolve each other by name (DNS)", "It makes containers run faster", "It removes the need for port publishing", "It gives containers direct host network access"], "correct_answer": "Containers can resolve each other by name (DNS)", "competency": "Networking", "difficulty": "beginner", "misconception_hint": "The default bridge lacks a feature that makes service-to-service addressing fragile."},
            {"id": "n2", "type": "mcq", "question": "Which command creates a new Docker network?", "options": ["docker network create appnet", "docker create network appnet", "docker net add appnet", "docker bridge create appnet"], "correct_answer": "docker network create appnet", "competency": "Networking", "difficulty": "beginner", "misconception_hint": "The CLI follows the same resource-verb pattern as volumes and containers."},
            {"id": "n3", "type": "mcq", "question": "In a user-defined network, how does a web container reach a database container named `db`?", "options": ["Using the hostname `db`", "Using the host's IP address", "By sharing the same writable layer", "Through `docker exec` only"], "correct_answer": "Using the hostname `db`", "competency": "Networking", "difficulty": "beginner", "misconception_hint": "User-defined networks provide DNS resolution for container names."},
        ]
    },
    "locales": {
        "ar": {
            "learn": {
                "title": "الشبكات في Docker",
                "explanation": "افتراضيًا، كل حاوية ليها namespace شبكة منفصل. الحاويات على الـ bridge الافتراضي ممكن توصل بعضها بس عن طريق IP address، واللي بيتغيّر. الـ **user-defined bridge network** بتدي الحاويات أسماء من خلال DNS وعزل محكوم: الحاويات على نفس الشبكة ممكن تتكلم باسمها، بينما الحاويات غير المرتبطة بتفضل منفصلة.",
                "key_ideas": [
                    "الـ default bridge network مفيش فيه DNS؛ الحاويات بتتوصل ببعضها عن طريق IP، وده مش ثابت.",
                    "`docker network create appnet` بيعمل user-defined bridge network.",
                    "`docker run --network appnet --name web ...` بيدخل حاوية للشبكة دي.",
                    "الحاويات على نفس الـ user-defined network ممكن تستخدم أسماء بعضها، مثلًا `web` أو `db:5432`.",
                    "`docker network inspect appnet` بيوريك الحاويات المرتبطة وعناوين IP بتاعتها.",
                ],
                "key_terms": {"network namespace": "stack شبكة معزول (interfaces, routes, firewall rules) للحاوية.", "bridge network": "switch افتراضي جوه Docker بيوصّل الحاويات على نفس الجهاز.", "user-defined network": "شبكة bridge مخصصة بتتعمل بواسطة المستخدم، فيها DNS مدمج وعزل أفضل.", "DNS resolution": "إنك تلاقي الحاوية باسمها بدل ما تدور على IP address.", "service discovery": "إنك تلاقي خدمة تانية باسمها بدل IP متغيّر."},
                "job_relevance": "التطبيقات متعددة الخدمات (web + database + cache) محتاجة تواصل ثابت. الـ user-defined networks هي الطريقة القياسية لمنح الحاويات أسماء ثابتة وعزل stack التطبيق.",
                "real_world_example": "حاوية API محتاجة توصل لـ Postgres. لو هما على نفس شبكة اسمها `appnet`، الـ API ممكن يتصل بـ `postgres://db:5432/mydb`. لما حاوية Postgres تتعمل restart وتاخد IP جديد، الاسم لسه بيتحلّل صح.",
                "common_mistake": "ما تعتمدش على الـ default bridge للتواصل بين الخدمات: عناوين IP بتتغيّر ومفيش DNS. اعمل user-defined network واستخدم أسماء الحاويات كـ hostnames.",
                "worked_example": "المثال بيعمل شبكة، بيشغّل حاوية قاعدة بيانات وحاوية ويب عليها، وبيوضّح إزاي حاوية الـ web توصل لـ db بالاسم بدل IP.",
                "depth_note": "محتوى متوسط ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم الـ Docker CLI الحديث (Docker Engine 23 وما بعده). SkillBridge ما بينفّذش أوامر Docker.",
                "grounding_sources": [
                    {"title": "نظرة عامة على شبكات Docker", "url": "https://docs.docker.com/engine/network/", "source": "Docker documentation"},
                    {"title": "نظرة عامة على bridge network", "url": "https://docs.docker.com/engine/network/drivers/bridge/", "source": "Docker documentation"},
                ],
            },
            "example": {
                "title": "وصّل تطبيق ويب بقاعدة بيانات على نفس الشبكة",
                "type": "bash",
                "content": "# 1) create a user-defined bridge network\ndocker network create appnet\n\n# 2) run a database container on the network\ndocker run -d --name db --network appnet -e POSTGRES_PASSWORD=secret postgres:16\n\n# 3) run a web container on the same network, publishing its port\ndocker run -d --name web --network appnet -p 8080:80 myweb:1.0\n\n# 4) inspect the network to see attached containers\ndocker network inspect appnet\n\n# Inside the web container, the database is reachable at db:5432",
                "explanation": "الاتنين على `appnet`، فممكن يحلّلوا بعض بالاسم. حاوية الـ web مش محتاجة تعرف IP بتاع الـ database؛ بتستخدم `db:5432`. نشر `-p 8080:80` بيكشف خدمة الويب للـ host بس. مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "وصّل حاوية API بقاعدة بيانات بالاسم",
                "task": "محتاج حاوية API (`api`) توصل لـ Postgres (`db`) من غير ما تثبت IP address. اكتب الأوامر عشان: (١) تعمل user-defined bridge network اسمها `appnet`، (٢) تشغّل حاوية `db` على `appnet` مع كلمة سر محددة بـ environment variable، (٣) تشغّل حاوية `api` على `appnet` وتنشر بورت 8080 على الجهاز لبورت 3000 جوهها، و(٤) تورّي إزاي الـ API هيتصل بـ db باستخدام اسم الحاوية. اكتب كمان أمر `docker network inspect appnet` اللي هتستخدمه للتحقق إن الاتنين مرتبطين. SkillBridge بيراجع أوامرك كنص بس — مش بينفّذها.",
                "response_type": "command",
                "competency": "Networking",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من `docker network create appnet`، وأمرين `docker run` بيستخدموا `--network appnet` مع `--name db` و`--name api`، و`-e POSTGRES_PASSWORD=...`، و`-p 8080:3000`، وconnection string أو hostname بيستخدم `db` (مش IP)، و`docker network inspect appnet`. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتشرح ليه user-defined network أحسن من الـ default bridge للـ name resolution. الإجابة الضعيفة بتستخدم IP addresses، أو تنسى `--network`، أو تخلط بين نشر البورت والـ DNS الداخلي للحاويات.",
            },
            "mini_check": {"questions": [
                {"id": "n1", "question": "إيه أهم ميزة في user-defined bridge network مقارنة بالـ default bridge؟", "options": ["الحاويات ممكن تحلّل بعضها بالاسم (DNS)", "الحاويات بتشتغل أسرع", "بيلغي الحاجة لنشر البورتات", "بيدي الحاويات وصول مباشر لشبكة الـ host"], "misconception_hint": "الـ default bridge ناقصة ميزة بتخلي التواصل بين الخدمات غير ثابت."},
                {"id": "n2", "question": "أي أمر بيعمل شبكة Docker جديدة؟", "options": ["docker network create appnet", "docker create network appnet", "docker net add appnet", "docker bridge create appnet"], "misconception_hint": "الـ CLI بنفس نمط الـ resource-verb زي الـ volumes والحاويات."},
                {"id": "n3", "question": "في user-defined network، إزاي حاوية web توصل لحاوية database اسمها `db`؟", "options": ["باستخدام الـ hostname `db`", "باستخدام IP address بتاع الـ host", "بمشاركة نفس طبقة الكتابة", "عن طريق `docker exec` بس"], "misconception_hint": "الـ user-defined networks بتدي DNS resolution لأسماء الحاويات."},
            ]},
        },
    },
}


DOCKER_COMPOSE = {
    "status": "complete",
    "skill_aliases": ("docker", "docker & containers"),
    "competency": "Compose",
    "objective": "Define and run a multi-container application with a docker-compose.yml file using the modern docker compose plugin syntax.",
    "objectives": [
        "Explain when Docker Compose is preferable to many individual `docker run` commands.",
        "Write a `docker-compose.yml` file with services, images, ports, volumes, and environment variables.",
        "Start and stop a stack with `docker compose up -d` and `docker compose down`.",
        "View logs with `docker compose logs`.",
        "Use the modern `docker compose` plugin syntax instead of the legacy `docker-compose` command.",
    ],
    "prerequisites": [],
    "roadmap_rationale": (
        "Compose is the capstone Docker topic: it uses containers, images, ports, volumes, and networking "
        "together in one declarative file. It belongs after the individual building blocks are established."
    ),
    "learn": {
        "title": "Compose",
        "explanation": (
            "Docker Compose lets you describe a multi-container application in a single YAML file, "
            "`docker-compose.yml`. Instead of remembering many `docker run` commands, you declare services, "
            "their images, ports, volumes, environment variables, and networks, then start the whole stack "
            "with one command. Modern Docker uses the `docker compose` plugin (a space), not the older "
            "`docker-compose` binary."
        ),
        "key_ideas": [
            "A `docker-compose.yml` file describes one or more services and their relationships.",
            "`docker compose up -d` creates networks, volumes, and containers in the right order and starts them in the background.",
            "`docker compose down` stops and removes containers and networks; add `--volumes` to remove named volumes too.",
            "`docker compose logs` shows combined logs from all services, or a single service with `docker compose logs web`.",
            "Each service name becomes a DNS hostname on the Compose-created network, just like a user-defined bridge network.",
        ],
        "key_terms": {
            "compose": "A Docker tool that defines and runs multi-container applications from a YAML file.",
            "service": "One container definition inside a docker-compose.yml file.",
            "docker-compose.yml": "The declarative file that describes the application's services, networks, and volumes.",
            "docker compose": "The modern Docker CLI plugin command (space between words).",
            "stack": "The collection of containers, networks, and volumes created by a Compose file.",
        },
        "job_relevance": (
            "Most real projects run more than one container. Compose is the standard way to define local "
            "development environments and small deployments so the whole team starts the same stack with one command."
        ),
        "real_world_example": (
            "A new developer clones the repository and runs `docker compose up -d`. One command starts the "
            "web service, the API, and the database, all on the same network with the right volumes and "
            "environment variables. There is no need to copy five separate `docker run` commands from a README."
        ),
        "common_mistake": (
            "Do not use the legacy `docker-compose` command in new workflows. Modern Docker installs provide "
            "`docker compose` (two words, a CLI plugin) with better integration and consistency."
        ),
        "worked_example": (
            "The example defines a web service and a database service in docker-compose.yml, starts them in "
            "the background, checks logs, and tears the stack down."
        ),
        "depth_note": "Canonical advanced content; it is fixed by the curated knowledge base, not generated for a target role.",
        "version_note": (
            "Examples use Compose file format 3.8 and the modern `docker compose` CLI plugin. SkillBridge does "
            "not execute Docker commands."
        ),
        "grounding_sources": [
            {"title": "Docker Compose overview", "url": "https://docs.docker.com/compose/", "source": "Docker documentation"},
            {"title": "Compose file reference", "url": "https://docs.docker.com/reference/compose-file/", "source": "Docker documentation"},
        ],
    },
    "example": {
        "title": "Run a web service and database with Compose",
        "type": "bash",
        "content": (
            "# docker-compose.yml\n"
            "version: \"3.8\"\n"
            "services:\n"
            "  db:\n"
            "    image: postgres:16\n"
            "    environment:\n"
            "      POSTGRES_PASSWORD: secret\n"
            "    volumes:\n"
            "      - pgdata:/var/lib/postgresql/data\n"
            "  web:\n"
            "    image: myweb:1.0\n"
            "    ports:\n"
            "      - \"8080:80\"\n"
            "    depends_on:\n"
            "      - db\n"
            "volumes:\n"
            "  pgdata:\n"
            "\n"
            "# Start the stack in the background\n"
            "docker compose up -d\n"
            "\n"
            "# View logs\n"
            "docker compose logs\n"
            "\n"
            "# Stop and remove containers and networks\n"
            "docker compose down"
        ),
        "explanation": (
            "The YAML file replaces several `docker run` commands. Compose creates the network and volume, "
            "starts the database, then starts the web service, and makes `db` reachable by name from `web`. "
            "Worked example for reading — SkillBridge does not run these commands."
        ),
    },
    "practice": {
        "type": "practical",
        "title": "Write a Compose file for a Node.js app and Postgres",
        "task": (
            "Write a `docker-compose.yml` file for a small Node.js API (`api`) and a Postgres database (`db`). "
            "Requirements: (1) Use Compose file version `3.8`, (2) define a `db` service using image `postgres:16` "
            "with environment variable `POSTGRES_PASSWORD=secret` and a named volume `pgdata` mounted at "
            "`/var/lib/postgresql/data`, (3) define an `api` service using image `myapi:1.0` that publishes host "
            "port 8080 to container port 3000 and depends on `db`, (4) declare the `pgdata` volume at the top level, "
            "(5) write the commands to start the stack in the background and view logs, (6) write the command to "
            "stop and remove everything including volumes. Use modern `docker compose` syntax (not `docker-compose`). "
            "SkillBridge reviews your YAML and commands as text only — it never executes them."
        ),
        "response_type": "configuration",
        "competency": "Compose",
        "evaluation_note": (
            "Static text review only: SkillBridge checks for `version: \"3.8\"`, two services (`db`, `api`), "
            "`image`, `environment`, `volumes`, `ports`, and `depends_on`, top-level `volumes:`, `docker compose up -d`, "
            "`docker compose logs`, and `docker compose down --volumes`, all using the modern `docker compose` form. "
            "It does not run Docker, so the review cannot prove runtime results. A strong answer keeps the YAML "
            "indentation consistent and explains why `depends_on` only controls start order, not readiness. A weak "
            "answer uses the legacy `docker-compose` command, omits the volume declaration, or mixes up host and container ports."
        ),
    },
    "mini_check": {
        "questions": [
            {"id": "c1", "type": "mcq", "question": "Which command starts a Compose stack in the background using the modern plugin syntax?", "options": ["docker compose up -d", "docker-compose up -d", "docker compose start", "docker run compose up"], "correct_answer": "docker compose up -d", "competency": "Compose", "difficulty": "beginner", "misconception_hint": "Modern Docker uses a CLI plugin with a space, not the legacy hyphenated binary."},
            {"id": "c2", "type": "mcq", "question": "In a docker-compose.yml, what does `depends_on` do?", "options": ["Controls service start order only", "Waits until a service is healthy before starting", "Creates a shared volume", "Publishes ports"], "correct_answer": "Controls service start order only", "competency": "Compose", "difficulty": "beginner", "misconception_hint": "It does not guarantee the dependency is ready to accept traffic."},
            {"id": "c3", "type": "mcq", "question": "How do containers in a Compose project reach each other by name?", "options": ["Compose creates a user-defined network with DNS", "They share the host network", "They must use published host ports", "They use the default bridge with IP addresses"], "correct_answer": "Compose creates a user-defined network with DNS", "competency": "Compose", "difficulty": "beginner", "misconception_hint": "Compose automatically provides the same name-resolution feature as a user-defined bridge network."},
        ]
    },
    "locales": {
        "ar": {
            "learn": {
                "title": "Docker Compose",
                "explanation": "Docker Compose بيسمح لك توصف تطبيق متعدد الحاويات في ملف YAML واحد، `docker-compose.yml`. بدل ما تفتكر كام أمر `docker run`، بتصرّح بالـ services والصور والبورتات والـ volumes والـ environment variables، وبعدين تشغّل الـ stack كله بأمر واحد. Docker الحديث بيستخدم `docker compose` plugin (مسافة)، مش الـ `docker-compose` binary القديم.",
                "key_ideas": [
                    "ملف `docker-compose.yml` بيوصف واحد أو أكتر من services وعلاقتهم ببعض.",
                    "`docker compose up -d` بيعمل الشبكات والـ volumes والحاويات بالترتيب الصح ويشغّلها في الخلفية.",
                    "`docker compose down` بيوقف ويمسح الحاويات والشبكات؛ ضيف `--volumes` عشان تمسح الـ named volumes كمان.",
                    "`docker compose logs` بيوريك الـ logs المجمعة من كل الخدمات، أو خدمة واحدة بـ `docker compose logs web`.",
                    "كل اسم service بيتحوّل لـ DNS hostname على الشبكة اللي Compose بيعملها، زي user-defined bridge network بالظبط.",
                ],
                "key_terms": {"compose": "أداة Docker بتعرف وتشغّل تطبيقات متعددة الحاويات من ملف YAML.", "service": "تعريف حاوية واحدة جوه ملف docker-compose.yml.", "docker-compose.yml": "الملف التصريحي اللي بيوصف services وnetworks وvolumes بتاعة التطبيق.", "docker compose": "أمر الـ Docker CLI plugin الحديث (كلمتين منفصلين).", "stack": "مجموعة الحاويات والشبكات والـ volumes اللي بيعملها ملف Compose."},
                "job_relevance": "أغلب المشاريع الحقيقية بتشغّل أكتر من حاوية. Compose هو الطريقة القياسية لتعريف بيئات التطوير المحلية والنشرات الصغيرة، عشان الفريق كله يشغّل نفس الـ stack بأمر واحد.",
                "real_world_example": "مطوّر جديد بيعمل clone للريبو ويشغّل `docker compose up -d`. أمر واحد بيشغّل خدمة الويب، والـ API، وقاعدة البيانات، كلهم على نفس الشبكة مع الـ volumes ومتغيرات البيئة الصح. مفيش حاجة تنسخ خمس أوامر `docker run` من README.",
                "common_mistake": "ما تستخدمش أمر `docker-compose` القديم في الـ workflows الجديدة. Docker الحديث بيوفر `docker compose` (كلمتين، CLI plugin) بتكامل أفضل واتساق أكتر.",
                "worked_example": "المثال بيعرّف خدمة web وخدمة database في docker-compose.yml، يشغّلهم في الخلفية، يتحقق من الـ logs، ويمسح الـ stack.",
                "depth_note": "محتوى متقدم ثابت من قاعدة المعرفة المراجَعة، مش محتوى مولّد حسب الوظيفة.",
                "version_note": "الأمثلة تستخدم Compose file format 3.8 وmodern `docker compose` CLI plugin. SkillBridge ما بينفّذش أوامر Docker.",
                "grounding_sources": [
                    {"title": "نظرة عامة على Docker Compose", "url": "https://docs.docker.com/compose/", "source": "Docker documentation"},
                    {"title": "مرجع ملف Compose", "url": "https://docs.docker.com/reference/compose-file/", "source": "Docker documentation"},
                ],
            },
            "example": {
                "title": "شغّل خدمة ويب وقاعدة بيانات بـ Compose",
                "type": "bash",
                "content": "# docker-compose.yml\nversion: \"3.8\"\nservices:\n  db:\n    image: postgres:16\n    environment:\n      POSTGRES_PASSWORD: secret\n    volumes:\n      - pgdata:/var/lib/postgresql/data\n  web:\n    image: myweb:1.0\n    ports:\n      - \"8080:80\"\n    depends_on:\n      - db\nvolumes:\n  pgdata:\n\n# Start the stack in the background\ndocker compose up -d\n\n# View logs\ndocker compose logs\n\n# Stop and remove containers and networks\ndocker compose down",
                "explanation": "ملف YAML بيحلّ محل كام أمر `docker run`. Compose بيعمل الشبكة والـ volume، يشغّل قاعدة البيانات، وبعدين يشغّل خدمة الويب، ويخلي `db` تتوصل بالاسم من `web`. مثال للقراية — SkillBridge ما بينفّذش الأوامر دي.",
            },
            "practice": {
                "title": "اكتب Compose file لتطبيق Node.js وPostgres",
                "task": "اكتب ملف `docker-compose.yml` لتطبيق Node.js API (`api`) وقاعدة بيانات Postgres (`db`). المتطلبات: (١) استخدم Compose file version `3.8`، (٢) عرّف خدمة `db` بصورة `postgres:16` ومتغير بيئة `POSTGRES_PASSWORD=secret` وnamed volume `pgdata` مركّب على `/var/lib/postgresql/data`، (٣) عرّف خدمة `api` بصورة `myapi:1.0` تنشر بورت 8080 على الجهاز لبورت 3000 جوهها وتعتمد على `db`، (٤) صرّح عن الـ volume `pgdata` على مستوى أعلى، (٥) اكتب الأوامر اللي تشغّل الـ stack في الخلفية وتوري الـ logs، (٦) اكتب الأمر اللي يوقف ويمسح كل حاجة بما فيها الـ volumes. استخدم صيغة `docker compose` الحديثة (مش `docker-compose`). SkillBridge بيراجع الـ YAML والأوامر كنص بس — مش بينفّذهم.",
                "response_type": "configuration",
                "competency": "Compose",
                "evaluation_note": "مراجعة نصية ثابتة فقط: SkillBridge بيتأكد من `version: \"3.8\"`، وخدمتين (`db` و`api`)، و`image` و`environment` و`volumes` و`ports` و`depends_on`، وإعلان `volumes:` على المستوى الأعلى، و`docker compose up -d` و`docker compose logs` و`docker compose down --volumes`، كلهم بصيغة `docker compose` الحديثة. مش بيشغّل Docker، فالمراجعة ما بتثبتش نتيجة تشغيل. الإجابة القوية بتحافظ على مسافات الـ YAML متسقة وبتشرح ليه `depends_on` بيتحكم في ترتيب التشغيل بس مش في الجاهزية. الإجابة الضعيفة بتستخدم أمر `docker-compose` القديم، أو بتنسى إعلان الـ volume، أو بتخلط بين بورت الجهاز والحاوية.",
            },
            "mini_check": {"questions": [
                {"id": "c1", "question": "أي أمر بيشغّل Compose stack في الخلفية باستخدام الـ plugin الحديث؟", "options": ["docker compose up -d", "docker-compose up -d", "docker compose start", "docker run compose up"], "misconception_hint": "Docker الحديث بيستخدم CLI plugin بمسافة، مش الـ binary القديم اللي فيه hyphen."},
                {"id": "c2", "question": "في docker-compose.yml، إيه اللي بيعمله `depends_on`؟", "options": ["بيتحكم في ترتيب تشغيل الخدمات بس", "بيستنى لحد ما الخدمة تبقى healthy قبل التشغيل", "بينشئ shared volume", "بينشر البورتات"], "misconception_hint": "مش بيضمن إن الـ dependency جاهز يستقبل ترافيك."},
                {"id": "c3", "question": "إزاي الحاويات في مشروع Compose بتوصل بعضها بالاسم؟", "options": ["Compose بيعمل user-defined network مع DNS", "بيتشاركوا شبكة الـ host", "لازم يستخدموا published host ports", "بيتخدموا default bridge مع IP addresses"], "misconception_hint": "Compose بيوفر تلقائيًا نفس ميزة name resolution اللي في user-defined bridge network."},
            ]},
        },
    },
}


def curated_diagnostic_questions(skill_name, competencies):
    """Return reviewed diagnostic questions for complete curated topics.

    Questions are authored against one canonical competency each.  This is
    intentionally narrower than the general skill-level bank: callers must
    never tag a question about one Python topic as another merely for coverage.
    """
    requested = {_key(item) for item in (competencies or [])}
    skill_key = _key(skill_name)
    banks = {
        "python functions": [
            {"type": "mcq", "question": "In `def add(a, b): return a + b`, what does `return` do?", "options": ["Displays the sum only", "Sends the sum back to the caller", "Defines a parameter", "Stops Python forever"], "correct_answer": "Sends the sum back to the caller", "competency": "python_functions", "difficulty": "beginner"},
            {"type": "mcq", "question": "In `def greet(name):`, `name` is a:", "options": ["parameter", "argument", "module", "exception"], "correct_answer": "parameter", "competency": "python_functions", "difficulty": "beginner"},
            {"type": "mcq", "question": "Which call correctly supplies two arguments to `delivery_total(price, delivery_fee)`?", "options": ["delivery_total(20, 5)", "delivery_total(price)", "def delivery_total(20, 5)", "return delivery_total"], "correct_answer": "delivery_total(20, 5)", "competency": "python_functions", "difficulty": "beginner"},
        ],
        "python error handling": [
            {"type": "mcq", "question": "Which exception can `int(\"eighty\")` raise?", "options": ["ValueError", "KeyError", "ImportError", "No exception"], "correct_answer": "ValueError", "competency": "python_error_handling", "difficulty": "beginner"},
            {"type": "mcq", "question": "Where should `int(text)` go when it may fail because the text is not numeric?", "options": ["Inside `try`", "Only inside `except ValueError`", "After `return None`", "Inside a bare `except`"], "correct_answer": "Inside `try`", "competency": "python_error_handling", "difficulty": "beginner"},
            {"type": "mcq", "question": "Why catch `ValueError` rather than using bare `except:` in `parse_score`?", "options": ["It handles invalid numeric text without hiding unrelated bugs", "It converts every string", "It avoids using return", "It executes faster"], "correct_answer": "It handles invalid numeric text without hiding unrelated bugs", "competency": "python_error_handling", "difficulty": "beginner"},
],
        # Docker Batch 1 — curated diagnostic banks for the topics that are complete.
        # These SUPPLEMENT the AI fallback; uncovered Docker competencies still get
        # AI-generated (or deterministic fallback) questions so all 11 blueprint
        # topics are represented.
        "containers": [
            {"type": "mcq", "question": "Which command lists containers that have already stopped?", "options": ["docker ps", "docker ps -a", "docker logs", "docker images"], "correct_answer": "docker ps -a", "competency": "containers", "difficulty": "beginner"},
            {"type": "mcq", "question": "What is true right after `docker stop web` finishes?", "options": ["It is deleted from disk immediately", "It still exists and can be started again with `docker start web`", "Its image is removed too", "It restarts automatically"], "correct_answer": "It still exists and can be started again with `docker start web`", "competency": "containers", "difficulty": "beginner"},
            {"type": "mcq", "question": "In `docker run -d --name web -p 8080:80 nginx:1.27`, what does `-d` do?", "options": ["Runs the container in the background (detached)", "Deletes the container when it exits", "Publishes port 8080", "Pins the image by digest"], "correct_answer": "Runs the container in the background (detached)", "competency": "containers", "difficulty": "beginner"},
        ],
        "images": [
            {"type": "mcq", "question": "What does `docker pull nginx` (no tag) actually download?", "options": ["The `nginx:latest` tag — whichever version it points to today", "Every tag in the repository", "Only the smallest layer", "A digest-pinned snapshot"], "correct_answer": "The `nginx:latest` tag — whichever version it points to today", "competency": "images", "difficulty": "beginner"},
            {"type": "mcq", "question": "Why can `docker rmi nginx:1.27` fail even when the command is typed correctly?", "options": ["A container — even a stopped one — still uses that image", "Images can never be removed", "`rmi` only works on dangling images", "Docker must be stopped first"], "correct_answer": "A container — even a stopped one — still uses that image", "competency": "images", "difficulty": "beginner"},
            {"type": "mcq", "question": "Two images stored locally share most of their layers. What does that mean for disk space?", "options": ["The shared layers are stored once, not duplicated per image", "Each image keeps a full private copy", "The layers are compressed twice", "Docker deletes the older image automatically"], "correct_answer": "The shared layers are stored once, not duplicated per image", "competency": "images", "difficulty": "beginner"},
        ],
        # Docker Batch 2 — one reviewed diagnostic question per newly complete topic.
        # Containers and Images keep their 3-question banks above.
        "basic commands": [
            {"type": "mcq", "question": "Which flag removes a container automatically after it exits?", "options": ["--rm", "-d", "-p", "--name"], "correct_answer": "--rm", "competency": "basic_commands", "difficulty": "beginner"},
        ],
        "dockerfile": [
            {"type": "mcq", "question": "Which Dockerfile instruction sets the base image?", "options": ["FROM", "COPY", "RUN", "CMD"], "correct_answer": "FROM", "competency": "dockerfile", "difficulty": "beginner"},
        ],
        "ports": [
            {"type": "mcq", "question": "Which `docker run` flag publishes a container port to the host?", "options": ["-p", "-d", "--name", "--rm"], "correct_answer": "-p", "competency": "ports", "difficulty": "beginner"},
        ],
        # Docker Batch 3 — one reviewed diagnostic question per newly complete topic.
        "volumes": [
            {"type": "mcq", "question": "What happens to data written in a container's writable layer when the container is removed?", "options": ["It is deleted", "It is copied into the image", "It moves to a volume automatically", "It stays forever"], "correct_answer": "It is deleted", "competency": "volumes", "difficulty": "beginner"},
        ],
        "networking": [
            {"type": "mcq", "question": "What is the main advantage of a user-defined bridge network over the default bridge?", "options": ["Containers can resolve each other by name (DNS)", "It makes containers run faster", "It removes the need for port publishing", "It gives containers direct host network access"], "correct_answer": "Containers can resolve each other by name (DNS)", "competency": "networking", "difficulty": "beginner"},
        ],
        "compose": [
            {"type": "mcq", "question": "Which command starts a Compose stack in the background using the modern plugin syntax?", "options": ["docker compose up -d", "docker-compose up -d", "docker compose start", "docker run compose up"], "correct_answer": "docker compose up -d", "competency": "compose", "difficulty": "beginner"},
        ],
    }
    if skill_key in PYTHON_FUNCTIONS["skill_aliases"]:
        out = []
        for key, questions in banks.items():
            if key in requested:
                out.extend(questions)
        return deepcopy(out)
    if skill_key in DOCKER_CONTAINERS["skill_aliases"]:
        out = []
        for key, questions in banks.items():
            if key in requested:
                out.extend(questions)
        return deepcopy(out)
    if skill_key in SQL_QUERIES_FILTERING["skill_aliases"] and any(
            key in requested for key in ("queries & filtering", "sql queries & filtering", "sql queries filtering")):
        return deepcopy([
            {"type": "mcq", "question": "Which clause filters rows to customers in Cairo?", "options": ["WHERE city = 'Cairo'", "SELECT city", "FROM Cairo", "ORDER BY city"], "correct_answer": "WHERE city = 'Cairo'", "competency": "sql_queries_filtering", "difficulty": "beginner"},
            {"type": "mcq", "question": "What does `SELECT name, email` return?", "options": ["The name and email columns", "Every column", "Only rows with email", "A new table"], "correct_answer": "The name and email columns", "competency": "sql_queries_filtering", "difficulty": "beginner"},
            {"type": "mcq", "question": "Which query reads active Cairo customers without changing data?", "options": ["SELECT name, email FROM customers WHERE city = 'Cairo' AND status = 'active';", "DELETE FROM customers WHERE city = 'Cairo';", "UPDATE customers SET status = 'active';", "INSERT INTO customers (city) VALUES ('Cairo');"], "correct_answer": "SELECT name, email FROM customers WHERE city = 'Cairo' AND status = 'active';", "competency": "sql_queries_filtering", "difficulty": "beginner"},
        ])
    return []


# These declarations reserve stable identifiers and schema for later curation.
# They are intentionally not served as lessons and must not be described as complete.
PLANNED_TOPICS = {
    ("sql", "joins"): {"status": "planned", "competency": "Joins", "prerequisites": ["Queries & filtering"], "content": None},
    ("machine learning", "evaluation basics"): {"status": "planned", "competency": "Evaluation basics", "prerequisites": ["Training a first model"], "content": None},
}


def complete_lesson(skill_name, competency):
    """Return a deep copy of canonical complete content, or ``None``."""
    if _key(skill_name) in PYTHON_FUNCTIONS["skill_aliases"] and _key(competency) == "python functions":
        return deepcopy(PYTHON_FUNCTIONS)
    if _key(skill_name) in PYTHON_ERROR_HANDLING["skill_aliases"] and _key(competency) in ("python error handling", "error handling"):
        return deepcopy(PYTHON_ERROR_HANDLING)
    if _key(skill_name) in SQL_QUERIES_FILTERING["skill_aliases"] and _key(competency) in (
            "queries & filtering", "sql queries & filtering", "sql queries filtering"):
        return deepcopy(SQL_QUERIES_FILTERING)
    if _key(skill_name) in DOCKER_CONTAINERS["skill_aliases"] and _key(competency) in ("containers", "docker containers"):
        return deepcopy(DOCKER_CONTAINERS)
    if _key(skill_name) in DOCKER_IMAGES["skill_aliases"] and _key(competency) in ("images", "docker images"):
        return deepcopy(DOCKER_IMAGES)
    if _key(skill_name) in DOCKER_BASIC_COMMANDS["skill_aliases"] and _key(competency) in ("basic commands", "basic commands"):
        return deepcopy(DOCKER_BASIC_COMMANDS)
    if _key(skill_name) in DOCKER_DOCKERFILE["skill_aliases"] and _key(competency) in ("dockerfile",):
        return deepcopy(DOCKER_DOCKERFILE)
    if _key(skill_name) in DOCKER_PORTS["skill_aliases"] and _key(competency) in ("ports",):
        return deepcopy(DOCKER_PORTS)
    if _key(skill_name) in DOCKER_VOLUMES["skill_aliases"] and _key(competency) in ("volumes",):
        return deepcopy(DOCKER_VOLUMES)
    if _key(skill_name) in DOCKER_NETWORKING["skill_aliases"] and _key(competency) in ("networking",):
        return deepcopy(DOCKER_NETWORKING)
    if _key(skill_name) in DOCKER_COMPOSE["skill_aliases"] and _key(competency) in ("compose",):
        return deepcopy(DOCKER_COMPOSE)
    return None


def prerequisites_for(skill_name, competency):
    topic = complete_lesson(skill_name, competency)
    return topic["prerequisites"] if topic else []
