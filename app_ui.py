import sqlite3
import streamlit as st
import pandas as pd
from PIL import Image
from app.ai_utils import SmartMenuAI
from app.recommender import recommend_by_mood
import os
from app.db import init_db

init_db()

st.set_page_config(page_title="SmartMenu AI", page_icon="🍔", layout="centered")
st.title("🍔 SmartMenu AI")

# --------- Load CSV ---------
try:
    menu = pd.read_csv("data/menu.csv")
    st.success("CSV loaded successfully!")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Show small preview
st.write("Full Menu:")
st.dataframe(menu)

# --------- UI controls ---------
mood = st.selectbox("How are you feeling today?", ["happy", "sad", "tired", "excited", "stressed"])
max_items = st.number_input(
    "Choose number of recommendations:",
    min_value=1,
    max_value=5,
    value=3,
    step=1
)


import os
st.write("Debug: GROQ_API_KEY detected?", bool(os.environ.get("GROQ_API_KEY")))

# Create AI client once (safe even if secrets are missing; we’ll show any error)
ai_client = None
ai_init_error = None
try:
    # Pick one:
    ai_client = SmartMenuAI(model="llama-3.1-70b-versatile")
except Exception as e:
    ai_init_error = str(e)
    ai_client = None


# ----------------------------- MAIN BUTTON -----------------------------
if st.button("Get Recommendations"):
    try:
        recs_df = recommend_by_mood(menu, mood)
        recs = pd.DataFrame(recs_df)

        if recs.empty:
            st.info("No recommendations found. Showing top popular items instead.")
            recs = menu.sort_values("popularity_score", ascending=False)

        recs = recs.head(max_items)

        # --- DB LOGGING ---
        from app.db import get_connection
        conn = get_connection()
        cur = conn.cursor()
        for dish_id in recs['id'].tolist():
            cur.execute("INSERT INTO user_history (mood, dish_id) VALUES (?, ?)", (mood, dish_id))
        conn.commit()
        conn.close()
        # --- END LOGGING ---

        # -------- DISPLAY EACH RECOMMENDATION ----------
        for _, row in recs.iterrows():
            st.markdown(f"### {row['name']} — {row.get('category','')} — ${row['price']}")
            st.write(row.get("description", ""))

            img_path = row.get("image", "")
            if img_path and os.path.exists(img_path):
                try:
                    st.image(Image.open(img_path), width=300)
                except:
                    st.text("[Could not load image]")
            else:
                st.text("[Image not available]")

            # ---- AI Explanation (Groq) ----
    with st.expander("Why AI recommends this dish? 🤖", expanded=False):
        if ai_client is None:
            msg = "AI explanation is disabled"
            if ai_init_error:
                msg += f" — {ai_init_error}"
            st.info(msg)
        else:
            try:
                top_names = recs['name'].tolist()
                prompt = (
                    f"The user feels {mood}. From these dishes {top_names}, "
                    "recommend one and explain in 2 concise sentences why it suits this mood."
                )
                st.write(ai_client.generate_response(prompt))
            except Exception as e:
                st.warning(f"AI explanation unavailable: {e}")
