from PIL import Image, ImageDraw, ImageFont
import os

# Output folder
out_dir = "../tiles"
os.makedirs(out_dir, exist_ok=True)

# Tile settings
tile_width, tile_height = 100, 150
font_size = int(tile_height * 0.525)
outer_border_thickness = 4
inner_border_thickness = 2
corner_radius = 15
inner_margin = 6  # margin for inner border

# Number colors
colors = {
    "cyan": (0, 200, 255),
    "red": (220, 0, 0),
    "black": (0, 0, 0),
    "yellow": (255, 200, 0)
}

# Load font
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)
except:
    font = ImageFont.load_default()

count = 0
for color_name, rgb in colors.items():
    for num in range(1, 14):
        # Create image with transparent background for rounded edges
        img = Image.new("RGBA", (tile_width, tile_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Outer rounded rectangle
        draw.rounded_rectangle(
            [(0, 0), (tile_width-1, tile_height-1)],
            radius=corner_radius,
            fill="white",
            outline="black",
            width=outer_border_thickness
        )

        # Inner border for depth
        draw.rounded_rectangle(
            [(inner_margin, inner_margin), (tile_width-1-inner_margin, tile_height-1-inner_margin)],
            radius=corner_radius - inner_margin,
            outline=(180, 180, 180),
            width=inner_border_thickness
        )

        # Center text
        text = str(num)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (tile_width - text_w) // 2 - bbox[0]
        y = (tile_height - text_h) // 2 - bbox[1]
        draw.text((x, y), text, font=font, fill=rgb)

        # Save image
        filename = os.path.join(out_dir, f"{color_name}_{num}.png")
        img.save(filename)
        count += 1

print(f"Saved {count} rounded tiles with inner border in '{out_dir}'.")
