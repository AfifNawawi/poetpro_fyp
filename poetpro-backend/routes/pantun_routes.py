from flask import Blueprint, request, jsonify
from utils.pantun_checker import analyze_pantun
from ml.pantun_ai_engine import PantunAIEngine

pantun_bp = Blueprint("pantun", __name__)
pantun_ai = PantunAIEngine()


@pantun_bp.route("/pantun/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    analysis = analyze_pantun(text)
    ai_result = pantun_ai.process_pantun(text)

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

    if status == "correct":
        return ai_result.get("message")

    if status in ["completed", "fixed"]:
        return ai_result.get("fixed_pantun")

    return "Tiada cadangan AI."


















