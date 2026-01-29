from ml.syair_ai_engine import SyairAIEngine

engine = SyairAIEngine()


def print_result(result):
    print("\n--- RESULT ---\n")

    status = result.get("status")

    if status == "completed":
        print("✅ Syair completed by AI:\n")
        print(result["completed_syair"])

    elif status == "fixed":
        print("✏️ Syair corrected by AI:\n")
        print(result["fixed_syair"])

    elif status == "correct":
        print("✔️ Syair already correct:\n")
        print(result["message"])

    else:
        print("❌ Error:")
        print(result.get("message"))


# =========================
# Test Case 1 — 1 line only
# =========================
syair_1 = "dengarlah kawan satu cerita"

print("\n=== TEST 1: Incomplete Syair (1 line) ===")
result = engine.process_syair(syair_1)
print_result(result)


# =========================
# Test Case 2 — 3 lines only
# =========================
syair_2 = """
dengarlah kawan satu cerita
seorang budak malas berusaha
setiap hari asyik tertidur
"""

print("\n=== TEST 2: Incomplete Syair (3 lines) ===")
result = engine.process_syair(syair_2)
print_result(result)


# =========================
# Test Case 3 — Wrong rhyme on line 3 only
# =========================
syair_3 = """
dengarlah kawan satu cerita
seorang budak malas berusaha
setiap hari asyik tertidur
enak bermimpi di pokok sena
"""

print("\n=== TEST 3: Wrong rhyme on line 3 ===")
result = engine.process_syair(syair_3)
print_result(result)


# =========================
# Test Case 4 — Correct syair
# =========================
syair_4 = """
dengarlah kawan satu cerita
seorang budak rajin berusaha
setiap hari belajar sentiasa
enak bermimpi di pokok sena
"""

print("\n=== TEST 4: Correct Syair ===")
result = engine.process_syair(syair_4)
print_result(result)
