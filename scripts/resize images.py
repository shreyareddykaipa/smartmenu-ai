from PIL import Image
import os

img_dir = "images"
target_w = 800

for fname in os.listdir(img_dir):
    if not fname.lower().endswith((".jpg",".jpeg",".png")):
        continue
    path = os.path.join(img_dir, fname)
    img = Image.open(path)
    w, h = img.size
    if w > target_w:
        new_h = int(target_w * h / w)
        img = img.resize((target_w, new_h), Image.LANCZOS)
        img.save(path, optimize=True, quality=85)
        print("Resized", fname)
    else:
        print("Skipped (small):", fname)
