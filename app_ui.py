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

# show small preview
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


if st.button("Get Recommendations"):
    try:
        recs_df = recommend_by_mood(menu, mood)  # your recommender
        recs = pd.DataFrame(recs_df)  # convert if needed

        if recs.empty:
            st.info("No recommendations found. Showing top popular items instead.")
            recs = menu.sort_values("popularity_score", ascending=False)

        # Apply user-selected number of recommendations
        recs = recs.head(max_items)

        # --- INSERT DB LOGGING HERE ---
        from app.db import get_connection

        conn = get_connection()
        cur = conn.cursor()
        for dish_id in recs['id'].tolist():
            cur.execute(
                "INSERT INTO user_history (mood, dish_id) VALUES (?, ?)",
                (mood, dish_id)
            )
        conn.commit()
        conn.close()
        # --- DB LOGGING END ---

        # Display recommendations with images
        for _, row in recs.iterrows():
            st.markdown(f"### {row['name']}  —  {row.get('category', '')}  —  ${row['price']}")
            st.write(row.get("description", ""))
            img_path = row.get("image", "")
            if img_path and os.path.exists(img_path):
                try:
                    st.image(Image.open(img_path), width=300)
                except:
                    st.text("[Could not load image]")
            else:
                st.text("[Image not available]")

       

        # AI explanation (optional)
        try:
            model_folder = r"C:/Users/shrey/AppData/Local/nomic.ai/GPT4All"
            model_file = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
            ai = SmartMenuAI(model_path=os.path.join(model_folder, model_file))
            top_names = recs['name'].tolist()
            prompt = f"The user feels {mood}. From these dishes {top_names}, recommend one and explain in 2 sentences why it suits this mood."
            explanation = ai.generate_response(prompt)
            st.subheader("AI Explanation")
            st.write(explanation)
        except Exception as e:
            st.warning(f"AI explanation unavailable: {e}")

    except Exception as e:
        st.error(f"Error during recommendations: {e}")
