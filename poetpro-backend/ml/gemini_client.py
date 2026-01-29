import os
from google import genai

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in environment variables")

        self.client = genai.Client(api_key=api_key)

        print("🔍 Detecting available Gemini models...")

        models = list(self.client.models.list())

        if not models:
            raise RuntimeError("❌ No Gemini models available for this API key")

        # Prefer flash models (fast & cheap)
        flash_models = [m.name for m in models if "flash" in m.name.lower()]
        pro_models = [m.name for m in models if "pro" in m.name.lower()]

        if flash_models:
            self.model = flash_models[0]
        elif pro_models:
            self.model = pro_models[0]
        else:
            self.model = models[0].name

        print(f"✅ Using Gemini model: {self.model}")

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text.strip()




