import os
from groq import Groq

class SmartMenuAI:
    """
    Cloud-friendly AI helper: uses Groq hosted LLM.
    Requires GROQ_API_KEY in Streamlit secrets or environment variable.
    """

    def __init__(self, model="llama-3.3-70b-versatile"):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GROQ_API_KEY")
            except Exception:
                api_key = None

        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set. Add it in Streamlit Secrets.")

        self.client = Groq(api_key=api_key)
        self.model = model  # store model name

    def generate_response(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()



