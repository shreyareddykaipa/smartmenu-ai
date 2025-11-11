import os
from groq import Groq

class SmartMenuAI:
    """
    Cloud-friendly AI helper: uses Groq hosted LLM.
    Requires GROQ_API_KEY in Streamlit secrets or env.
    """
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            # Streamlit automatically exposes st.secrets to env as well,
            # but we can do a secondary fallback:
            try:
                import streamlit as st
                api_key = st.secrets.get("GROQ_API_KEY")
            except Exception:
                api_key = None

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it in Streamlit Secrets."
            )

        self.client = Groq(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
