import random

rest = "\033[0m"
colors = [
        "\033[91m",
        "\033[92m",
        "\033[93m",
        "\033[94m",
        "\033[95m",
        "\033[96m"
        ]


def colorText(color, text, rest):
  print(f"{color}{text}{rest}")

def clear_screen():
  # For Windows
  if os.name == 'nt':
      _ = os.system('cls')
  # For macOS and Linux
  else:
      _ = os.system('clear')


