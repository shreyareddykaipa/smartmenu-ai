# scripts/preview_menu.py
import streamlit as st
import pandas as pd

st.title("Menu Preview")
menu = pd.read_csv("data/menu.csv")

for _, row in menu.iterrows():
    st.markdown(f"### {row['name']} — ${row['price']:.2f}")
    st.write(row['description'])
    st.write("Tags:", row['tags'])
    try:
        st.image(row['image'], width=300)
    except Exception as e:
        st.error(f"Image load error: {row['image']} — {e}")
    st.divider()
