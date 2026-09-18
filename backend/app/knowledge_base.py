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
        # Note: Docker containers/images diagnostic banks temporarily removed to
        # restore full 11-topic diagnostic coverage via fallback path.
        # Curated lesson content (DOCKER_CONTAINERS, DOCKER_IMAGES) remains intact.
        # Re-add when Eslam decides whether curated banks should replace or
        # supplement fallback diagnostic questions.
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
    return None


def prerequisites_for(skill_name, competency):
    topic = complete_lesson(skill_name, competency)
    return topic["prerequisites"] if topic else []
