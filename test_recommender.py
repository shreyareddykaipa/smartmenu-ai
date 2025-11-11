from app.ai_utils import SmartMenuAI
from app.recommender import recommend_by_mood

ai = SmartMenuAI(
    model_path=r"C:\Users\shrey\AppData\Local\nomic.ai\GPT4All\Meta-Llama-3-8B-Instruct.Q4_0.gguf"
)

menu = ai.load_menu("data/menu.csv")

mood = input("How are you feeling today? ")

recs = recommend_by_mood(menu, mood)

print("\n--- AI Suggestions Based on Mood ---")
for r in recs:
    print(f"{r['name']}  -  {r['category']}  (${r['price']})")

prompt = f"""
The user is feeling {mood}.
Suggest 1 dish from this list: {menu['name'].tolist()}.
Explain why it matches the mood in 3 sentences.
"""

ai_response = ai.generate_response(prompt)

print("\n--- AI Explanation ---")
print(ai_response)
