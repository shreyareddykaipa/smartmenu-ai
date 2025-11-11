import pandas as pd
import os
from PIL import Image

menu = pd.read_csv("data/menu.csv")
errors = []

# Check image files exist
for idx, row in menu.iterrows():
    img_path = row['image']
    if not os.path.exists(img_path):
        errors.append(f"Missing image for id {row['id']}: {img_path}")

# Check numeric columns
for col in ['calories','price','prep_time_minutes','popularity_score','id']:
    if menu[col].isnull().any():
        errors.append(f"Null values found in {col}")

print("Rows:", len(menu))
if errors:
    print("Errors found:")
    for e in errors:
        print("-", e)
else:
    print("All good! Images present and CSV looks fine.")
