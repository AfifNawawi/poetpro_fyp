from ml.pantun_ai_engine import PantunAIEngine

engine = PantunAIEngine()


def print_result(result):
    print("\n--- RESULT ---\n")

    if result["status"] == "completed":
        print(result["completed_pantun"])

    elif result["status"] in ["fixed_line_3", "fixed_line_4"]:
        print(result["fixed_pantun"])

    elif result["status"] == "correct":
        print(result["message"])

    else:
        print("Error:", result["message"])


# =========================
# Test Case 1 — 1 line only
# =========================
pantun_1 = "Bunga melati di taman, indah"

print("\n=== TEST 1: Incomplete Pantun (1 line) ===")
result = engine.process_pantun(pantun_1)
print_result(result)


# =========================
# Test Case 2 — Line 3 wrong
# =========================
pantun_2 = """
jalan-jalan ke kota bandung,
jangan lupa mengisi saku,
kalau kamu sedang makan,
jangan lupa membaca buku.
"""

print("\n=== TEST 2: Wrong rhyme on line 3 ===")
result = engine.process_pantun(pantun_2)
print_result(result)


# =========================
# Test Case 3 — Line 4 wrong
# =========================
pantun_3 = """
Badan sihat minum jamu,
berbondong terbang burung belibis,
isilah akal dengan ilmu,
ilmu takkan pernah cukup.
"""

print("\n=== TEST 3: Wrong rhyme on line 4 ===")
result = engine.process_pantun(pantun_3)
print_result(result)


# =========================
# Test Case 4 — Correct pantun
# =========================
pantun_4 = """
Buah cempedak di luar pagar,
Ambil galah tolong jolokkan,
Saya budak baru belajar,
Kalau salah tolong tegurkan.
"""

print("\n=== TEST 4: Correct Pantun ===")
result = engine.process_pantun(pantun_4)
print_result(result)

