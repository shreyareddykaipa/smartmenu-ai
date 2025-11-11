# app/ai_utils.py
import os
from groq import Groq

class SmartMenuAI:
    """
    Cloud-friendly AI helper using Groq hosted LLMs.
    Requires GROQ_API_KEY set in environment or Streamlit secrets.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        # 1) Try env var first (works locally and on Streamlit Cloud)
        api_key = os.environ.get("GROQ_API_KEY")

        # 2) Fallback to st.secrets if available
        if not api_key:
            try:
                import streamlit as st  # imported lazily to avoid hard dependency here
                api_key = st.secrets.get("GROQ_API_KEY")
            except Exception:
                api_key = None

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to Streamlit Secrets or your environment."
            )

        self.client = Groq(api_key=api_key)
        # Use a currently supported model. Options include:
        #   - "llama-3.1-8b-instant"   (fast & inexpensive)
        #   - "llama-3.3-70b-versatile" (higher quality, more cost)
        self.model = model

    def generate_response(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()


