import re
from ml.pantun_retriever import PantunRetriever
from ml.gemini_client import GeminiClient
from utils.pantun_checker import analyze_pantun


class PantunAIEngine:
    def __init__(self):
        print("🤖 Initializing Pantun AI Engine...")
        self.retriever = PantunRetriever()
        self.gemini = GeminiClient()

    # ----------------------------
    # Helpers
    # ----------------------------
    def _get_lines(self, text):
        return [l.strip() for l in text.split("\n") if l.strip()]

    def _format_output(self, pantun_text):
        return f"Berikut adalah pantun yang telah diperbaiki:\n\n{pantun_text}"

    # ----------------------------
    # AI generation helpers
    # ----------------------------
    def _generate_fixed_pantun(self, prompt):
        pantun = self.gemini.generate(prompt).strip()
        return self._format_output(pantun)

    # ----------------------------
    # Complete or fix pantun
    # ----------------------------
    def _complete_or_fix_pantun(self, lines):
        user_text = "\n".join(lines[:4])

        references = self.retriever.search(user_text, top_k=5)
        ref_pantuns = [r["pantun"] for r in references]

        prompt = f"""
You are a Malay pantun expert.

User pantun:
{user_text}

Reference pantuns:
{chr(10).join(ref_pantuns)}

TASK:
- Ensure pantun has exactly 4 lines
- Ensure ABAB rhyme
- Fix any wrong rhyme lines
- Fix grammar if needed
- Keep original meaning and theme

Output ONLY the corrected 4-line pantun.
"""

        return self._generate_fixed_pantun(prompt)

    # ----------------------------
    # Main pipeline
    # ----------------------------
    def process_pantun(self, pantun_text):
        raw_lines = self._get_lines(pantun_text)

        # Case: More than 4 lines → keep first 4 only
        if len(raw_lines) > 4:
            raw_lines = raw_lines[:4]

        analysis = analyze_pantun("\n".join(raw_lines))

        # Case 1 — Less than 4 lines → complete pantun
        if len(raw_lines) < 4:
            fixed = self._complete_or_fix_pantun(raw_lines)
            return {
                "status": "completed",
                "fixed_pantun": fixed
            }

        # Case 2 — Correct pantun
        if analysis["issue_type"] == "correct":
            return {
                "status": "correct",
                "message": "Pantun anda sudah betul dan menepati format tradisional."
            }

        # Case 3 — Any rhyme error (line 3, line 4, or both)
        fixed = self._complete_or_fix_pantun(raw_lines)
        return {
            "status": "fixed",
            "fixed_pantun": fixed
        }






