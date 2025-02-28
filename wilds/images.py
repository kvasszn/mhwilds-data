import os
from PIL import Image
import numpy as np

base = os.environ["BASE"]
if version := os.environ["VERSION"]:
    pass
else:
    version = 241106027

def multiply_image_by_color(img, color):
    img = img.convert("RGBA")  # Ensure it has an alpha channel
    img_array = np.array(img, dtype=np.float32)  # Convert to float for multiplication
    img_array[..., :3] *= np.array(color, dtype=np.float32) / 255.0  # Normalize color
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)  # Clip and convert back to uint8
    return Image.fromarray(img_array, "RGBA")

def split_spritesheet(image_path, width, height, sprite_width=None, sprite_height=None, offset_x=0, offset_y=0):
    if sprite_width is None:
        sprite_width = width
    if sprite_height is None:
        sprite_height = height 
    img = Image.open(image_path)
    img_width, img_height = img.size
    cols = img_width // width
    rows = img_height // height
    sprites = []
    for row in range(rows):
        for col in range(cols):
            left = col * width + offset_x
            top = row * height + offset_y
            right = left + sprite_width
            bottom = top + sprite_height
            sprite = img.crop((left, top, right, bottom))
            sprites.append(sprite)
    return sprites

def add_padding(img, padding, color=(0, 0, 0, 0)):
    img = img.convert("RGBA")  # Ensure transparency is preserved
    new_size = (img.width + 2 * padding, img.height + 2 * padding)
    new_img = Image.new("RGBA", new_size, color)
    new_img.paste(img, (padding, padding), img)
    return new_img

def combine_images_horz(imgs, offset):
    width = sum([img.width + offset for img in imgs])
    height = max([img.height for img in imgs])
    combined = Image.new('RGBA', (width, height))
    x, y = 0, 0
    for img in imgs:
        combined.paste(img, (x, y))
        x += img.width + offset
    return combined


icon_dim = 100
ICONS_TEX = split_spritesheet(os.path.join(base, f"natives/STM/GUI/ui_texture/tex000000/tex000201_0_IMLM4.tex.{version}.png"), icon_dim, icon_dim)
add_icon_dim = 64
ADD_ICONS_TEX = split_spritesheet(os.path.join(base, f"natives/STM/GUI/ui_texture/tex000000/tex000201_20_IMLM4.tex.{version}.png"), add_icon_dim, add_icon_dim)
icon_dim = 100
COL_ICONS = split_spritesheet(os.path.join(base, f"natives/STM/GUI/ui_texture/tex000000/tex000201_1_IMLM4.tex.{version}.png"), icon_dim, icon_dim)

MAP_NUMS = split_spritesheet(os.path.join(base, f"natives/STM/GUI/ui_texture/tex060000/tex060002_04_IMLM4.tex.{version}.png"), 100, 100, 70, 100, (100-70)/2)

