from PIL import Image
import os
import colors as c
from datetime import datetime

# Ask user for image path
img_path = input("Enter image path or name (for working directory): ")

# Current timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M")

def resize_img():
    img = Image.open(img_path)
    img_format = img.format
    c.color(f"Format: {img_format}\nHeight: {img.height}\nWidth: {img.width}\n", 3)

    # Get new size
    size = input("Enter your required size (height,width): ")
    try:
        height, width = map(int, size.split(","))
    except ValueError:
        c.color("❌ Invalid size format. Use: height,width\n", 0)
        return

    # Resize
    resized_img = img.resize((width, height))

    # Ensure extension
    ext = img_format.lower()
    resized_filename = f"resized_{timestamp}.{ext}"

    # Save resized image
    resized_img.save(resized_filename, img_format)
    c.color(f"✅ Resized image saved as {resized_filename}\n", 2)

# Run if image exists
if os.path.exists(img_path):
    resize_img()
else:
    c.color(f"❌ Error: image not found at {img_path}\n", 0)
