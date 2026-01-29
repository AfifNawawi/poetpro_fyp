from transformers import BertTokenizer, EncoderDecoderModel
import torch

MODEL_PATH = "ml/pantun_syair_recommender"

try:
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    model = EncoderDecoderModel.from_pretrained(MODEL_PATH)

    # REQUIRED for encoder-decoder
    model.config.decoder_start_token_id = tokenizer.cls_token_id
    model.config.pad_token_id = tokenizer.pad_token_id
    model.config.eos_token_id = tokenizer.sep_token_id

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    MODEL_READY = True
except Exception as e:
    print("⚠️ MODEL LOAD FAILED:", e)
    MODEL_READY = False


# -------------------------------------------------
# Centralized safe suggestion generator
# -------------------------------------------------
def generate_suggestion(poem_type, issue_type, text):
    """
    poem_type: pantun | syair
    """

    # 🔒 HARD FALLBACKS (rule-based safety net)
    fallback = {
        # Pantun
        ("pantun", "rhyme_error_line_3"):
            "The third line breaks the ABAB rhyme pattern. Consider changing its ending to match the first line.",
        ("pantun", "rhyme_error_line_4"):
            "The fourth line breaks the ABAB rhyme pattern. Consider changing its ending to match the second line.",

        # Syair
        ("syair", "rhyme_error"):
            "This syair does not follow the AAAA rhyme pattern. Consider revising the ending of the inconsistent line.",
        ("syair", "line_count_error"):
            "Syair requires at least 4 lines. Add one more line to complete the structure."
    }

    if not MODEL_READY:
        return fallback.get((poem_type, issue_type), "No suggestion available.")

    # -------------------------------------------------
    # HARD POEM-TYPE CONTROL (THIS FIXES YOUR BUG)
    # -------------------------------------------------
    if poem_type == "pantun":
        system_rule = (
            "You are a Pantun expert.\n"
            "Pantun ALWAYS uses ABAB rhyme.\n"
            "DO NOT mention AAAA.\n"
            "DO NOT mention Syair.\n"
        )
    elif poem_type == "syair":
        system_rule = (
            "You are a Syair expert.\n"
            "Syair ALWAYS uses AAAA rhyme.\n"
            "DO NOT mention ABAB.\n"
            "DO NOT mention Pantun.\n"
        )
    else:
        system_rule = ""

    prompt = (
        f"{system_rule}"
        f"Give ONE short correction suggestion only.\n"
        f"Issue: {issue_type}\n\n"
        f"Text:\n{text}\n"
    )

    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=30,
            num_beams=2,
            do_sample=False
        )

        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 🚨 SAFETY CHECK — prevent cross-poem contamination
        if poem_type == "pantun" and "AAAA" in result:
            return fallback.get((poem_type, issue_type))
        if poem_type == "syair" and "ABAB" in result:
            return fallback.get((poem_type, issue_type))

        return result

    except Exception as e:
        print("⚠️ GENERATION FAILED:", e)
        return fallback.get((poem_type, issue_type), "No suggestion available.")








