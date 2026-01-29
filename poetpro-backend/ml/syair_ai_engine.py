import re
from collections import Counter
from ml.syair_retriever import SyairRetriever
from ml.gemini_client import GeminiClient
from utils.syair_checker import analyze_syair


class SyairAIEngine:
    def __init__(self):
        print("🤖 Initializing Syair AI Engine...")
        self.retriever = SyairRetriever()
        self.gemini = GeminiClient()

    # ----------------------------
    # Helper: split lines safely
    # ----------------------------
    def _get_lines(self, text):
        return [l.strip() for l in text.split("\n") if l.strip()]

    # ----------------------------
    # Detect broken Malay sentence
    # ----------------------------
    def _is_incomplete_sentence(self, line):
        line = line.strip().lower()

        if len(line.split()) < 3:
            return True

        function_words = [
            "di", "ke", "dari", "yang", "dan", "atau", "untuk",
            "pada", "kepada", "dengan", "dalam", "sebagai",
            "oleh", "tentang", "antara", "hingga"
        ]

        last_word = re.sub(r"[^\w]", "", line.split()[-1])

        if last_word in function_words:
            return True

        modals = ["akan", "telah", "sudah", "sedang", "masih", "boleh", "mesti", "harus"]
        if last_word in modals:
            return True

        return False

    # ----------------------------
    # Case 1: Complete syair (1–3 lines)
    # ----------------------------
    def _complete_syair(self, lines):
        user_text = "\n".join(lines)
        references = self.retriever.search(user_text, top_k=5)

        prompt = f"""
You are a Malay syair expert.

The user has written an incomplete syair.

User lines:
{user_text}

Reference syairs:
{chr(10).join(references)}

TASK:
1. If any user line is grammatically incomplete, fix it first.
2. Then complete the syair into exactly 4 lines.
3. Follow traditional syair style.
4. Follow AAAA rhyme (all lines same rhyme).
5. Keep user's meaning and theme.

Output ONLY the full corrected 4-line syair.
"""
        return self.gemini.generate(prompt)

    # ----------------------------
    # Fix wrong rhyme lines (exactly 4 lines)
    # ----------------------------
    def _fix_wrong_lines(self, lines, rhyme_units):
        counter = Counter(rhyme_units)
        target_rhyme = counter.most_common(1)[0][0]

        references = self.retriever.search("\n".join(lines), top_k=5)

        prompt = f"""
You are a Malay syair expert.

The following syair must follow AAAA rhyme (all lines same rhyme).

Target rhyme: "{target_rhyme}"

Original syair:
{chr(10).join(lines)}

Reference syairs:
{chr(10).join(references)}

TASK:
- Keep all correct lines unchanged
- Rewrite ONLY the lines that do not follow the target rhyme
- Maintain original meaning
- Follow traditional syair style
- Ensure all lines end with the same rhyme

Output ONLY the corrected syair.
"""
        return self.gemini.generate(prompt)

    # ----------------------------
    # Case 3: Fix rhyme for MORE than 4 lines
    # ----------------------------
    def _fix_long_syair(self, lines, rhyme_units):
        counter = Counter(rhyme_units)
        target_rhyme = counter.most_common(1)[0][0]

        references = self.retriever.search("\n".join(lines), top_k=5)

        prompt = f"""
You are a Malay syair expert.

The following syair has more than 4 lines.
Traditional syair must use AAAA rhyme (all lines same rhyme).

Target rhyme: "{target_rhyme}"

Original syair:
{chr(10).join(lines)}

Reference syairs:
{chr(10).join(references)}

TASK:
- Keep the SAME number of lines
- Rewrite ONLY lines that break the rhyme
- Ensure ALL lines end with the same rhyme
- Maintain original meaning and grammar
- Follow traditional syair style

Output ONLY the corrected syair with the same number of lines.
"""
        return self.gemini.generate(prompt)

    # ----------------------------
    # Main pipeline
    # ----------------------------
    def process_syair(self, syair_text):
        lines = self._get_lines(syair_text)
        analysis = analyze_syair(syair_text)

        # Case 1 — Not enough lines (1–3)
        if len(lines) < 4:
            completed = self._complete_syair(lines)
            return {
                "status": "completed",
                "message": "Syair was incomplete. AI has completed it.",
                "original_lines": lines,
                "completed_syair": completed
            }

        # Case 2 — Correct syair
        if analysis["issue_type"] == "correct":
            return {
                "status": "correct",
                "message": "Syair structure and rhyme are correct.",
                "syair": syair_text
            }

        # Case 3 — More than 4 lines → keep all, fix rhyme
        if len(lines) > 4:
            fixed = self._fix_long_syair(lines, analysis["rhyme_units"])
            return {
                "status": "fixed_long_syair",
                "message": "Long syair corrected (AAAA rhyme enforced).",
                "original_syair": syair_text,
                "fixed_syair": fixed
            }

        # Case 4 — Exactly 4 lines but wrong rhyme
        fixed = self._fix_wrong_lines(lines, analysis["rhyme_units"])
        return {
            "status": "fixed",
            "message": "Syair corrected (wrong rhyme lines fixed).",
            "original_syair": syair_text,
            "fixed_syair": fixed
        }


