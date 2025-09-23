import os
import qrcode as qr
from PIL import Image
import colors as c

c.color("\t______ Welcome to QR-code-generator ______\n\tenter q or exit to end the program\n\n"
        "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")

# Default text
default = "hello world"

# Take input
text = input(f"Enter text to generate a QR code(default={default}): ").strip()
if not text:
  text = default
  c.color(f"QR code generated with text as '{default}'")

# Exit condition
if text in ["q", "exit"]:
  c.color("Have a nice day. Thanks :)\n")
  exit()

# Generate QR
img = qr.make(text)
img = img.resize((300, 300))  # Resize image
file = "qr"

# Check file existence
def check_exist(file):
  while os.path.exists(f"{file}.png"):
    c.color(f"error(1): file {file}.png exists in working directory. Please rename it.", 0)
    file = input("Enter a unique name: ").strip()
    if file in ["exit", "q"]:
      c.color("Have a nice day. Thanks :)\n")
      exit()
  img.save(f"{file}.png")
  c.color(f"QR code saved as {file}.png\n", 1)

check_exist(file)
