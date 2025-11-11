import random

def recommend_by_mood(menu_df, mood):
    suggestions = []

    mood_keywords = {
        "happy": ["burger", "wrap", "pizza"],
        "sad": ["brownie", "salad", "soup"],
        "tired": ["bowl", "fried rice"],
        "excited": ["tacos", "spicy"],
        "stress": ["tea", "soup", "salad"]
    }

    mood = mood.lower()

    if mood in mood_keywords:
        keywords = mood_keywords[mood]
        for key in keywords:
            matches = menu_df[menu_df["name"].str.contains(key, case=False)]
            if not matches.empty:
                suggestions.append(matches.sample(1).iloc[0])
    else:
        return menu_df.sample(3)

    if suggestions:
        return suggestions
    else:
        return menu_df.sample(3)
