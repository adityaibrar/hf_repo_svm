from PIL import Image
import os

img_dir = 'static/images'
images = ['air_mineral.png', 'energy_drink.png', 'kopi_hitam.png', 'matcha_latte.png']

imgs = []
for name in images:
    path = os.path.join(img_dir, name)
    try:
        img = Image.open(path).convert("RGBA")
        imgs.append(img)
    except Exception as e:
        print(f"Error opening {path}: {e}")

if not imgs:
    print("No images found.")
    exit(1)

# Resize all to roughly similar height for compositing
target_height = 400
resized_imgs = []
for img in imgs:
    aspect_ratio = img.width / img.height
    new_width = int(target_height * aspect_ratio)
    img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)
    resized_imgs.append(img)

# We want them in a tight "Inside Out" group.
# Let's say:
# Back row: air_mineral (left), kopi_hitam (right)
# Front row: energy_drink (center-left), matcha_latte (center-right)
# We will create a canvas large enough to hold them.
canvas_width = 800
canvas_height = 600
canvas = Image.new('RGBA', (canvas_width, canvas_height), (0,0,0,0))

# Positions: (x, y)
# 0: air mineral (back left)
# 1: energy drink (front left)
# 2: kopi hitam (back right)
# 3: matcha latte (front right)

# Let's place 0 and 2 in the back (higher Y and smaller or just higher Y)
canvas.paste(resized_imgs[0], (50, 50), resized_imgs[0])
canvas.paste(resized_imgs[2], (450, 50), resized_imgs[2])

# Place 1 and 3 in the front
canvas.paste(resized_imgs[1], (200, 150), resized_imgs[1])
canvas.paste(resized_imgs[3], (350, 150), resized_imgs[3])

# Save the output
out_path = os.path.join(img_dir, 'mascot.png')
canvas.save(out_path, format="PNG")
print(f"Saved combined image to {out_path}")
