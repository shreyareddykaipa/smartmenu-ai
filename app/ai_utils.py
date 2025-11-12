from groq import Groq
import os

class SmartMenuAI:
    def __init__(self, model="llama-3.1-70b-versatile"):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        # ✅ Do NOT pass 'proxies' or 'timeout' here — only api_key
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful food recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            return f"AI explanation unavailable: {e}"
