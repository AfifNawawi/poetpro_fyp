from flask import Blueprint, request, jsonify
from utils.syair_checker import analyze_syair
from ml.syair_ai_engine import SyairAIEngine

syair_bp = Blueprint("syair", __name__)

# Initialize AI Engine once
syair_ai = SyairAIEngine()


@syair_bp.route("/syair/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Rule-based analysis
    analysis = analyze_syair(text)

    # AI Engine (RAG + Gemini)
    ai_result = syair_ai.process_syair(text)

    response = {
        "line_count": analysis["line_count"],
        "structure": analysis["structure"],
        "rhyme_pattern": analysis["rhyme_pattern"],
        "message": analysis["message"],
        "ai_suggestion": format_ai_result(ai_result)
    }

    return jsonify(response), 200


def format_ai_result(ai_result):
    status = ai_result.get("status")

    # Already correct
    if status == "correct":
        return "Syair anda sudah betul dan menepati format tradisional AAAA."

    # Auto-completed (1–3 lines)
    if status == "completed":
        return (
            "Berikut adalah syair yang telah diperbaiki:\n\n"
            + ai_result.get("completed_syair", "")
        )

    # Fixed 4-line syair
    if status == "fixed":
        return (
            "Berikut adalah syair yang telah diperbaiki:\n\n"
            + ai_result.get("fixed_syair", "")
        )

    # Fixed long syair (5+ lines)
    if status == "fixed_long_syair":
        return (
            "Berikut adalah syair yang telah diperbaiki:\n\n"
            + ai_result.get("fixed_syair", "")
        )

    # Fallback
    return ai_result.get("message", "Tiada cadangan AI.")









