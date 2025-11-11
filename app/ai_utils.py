import os
from groq import Groq

class SmartMenuAI:
    """
    Cloud-friendly AI helper: uses Groq hosted LLM.
    Requires GROQ_API_KEY in Streamlit secrets or environment.
    """
    def __init__(self):
        # Try environment variable first
        api_key = os.environ.get("GROQ_API_KEY")

        # Then try Streamlit secrets (for cloud deployment)
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                api_key = None

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Go to Streamlit Cloud → Settings → Secrets."
            )

        self.client = Groq(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model="llama3.1-8b-instant",  # ✅ Updated model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
