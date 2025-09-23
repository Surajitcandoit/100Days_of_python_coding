import random
import os

rest = "\033[0m"
clrs = [
    "\033[91m",  # 0 Red
    "\033[92m",  # 1 Green
    "\033[93m",  # 2 Yellow
    "\033[94m",  # 3 Blue
    "\033[95m",  # 4 Magenta
    "\033[96m"   # 5 Cyan
]


def color(text, code_idx=2, end=rest):
    print(f"{clrs[code_idx]}{text}{end}")

msg = ["Welcome to Password generator.","With build in command\npass\t\t\tto generate a new password with length of 12","q or exit\t\t to exit from the program.\n\n\n"]

for i in msg:
  color(i)

def generate_pass(length=12):
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "1234567890"
    chars = "*#$@&-_+?!/:^=×|%[]{}()"
    all_chars = alpha + nums + chars

    # Ensure at least one char from each category
    password = [
        random.choice(alpha),
        random.choice(nums),
        random.choice(chars)
    ]

    # Fill remaining length
    password += random.choices(all_chars, k=length - len(password))
    random.shuffle(password)

    generated = "".join(password)
    print(generated)
    return generated


def add_pass2file(m):
    with open("passwords.txt", "a") as f:
        f.write(f"{m}\n")
    color("Password saved in passwords.txt", 1)


def del_AllPass():
    if os.path.exists("passwords.txt"):
        os.remove("passwords.txt")
        color("All passwords deleted.", 4)


def show_AllPass():
    if not os.path.exists("passwords.txt"):
        color("No saved passwords yet.", 0)
        return
    color("Generated passwords:", 1)
    with open("passwords.txt", "r") as f:
        for line in f:
            color(line.strip(), 5)


while True:
    cmd = input(f"{clrs[3]}cmd>> {rest}")
    if cmd in ["exit", "q"]:
        show_AllPass()
        del_AllPass()
        color("\n______________ Thank You _____________\n")
        break
    elif cmd == "pass":
        pw = generate_pass()
        add_pass2file(pw)
        print("")
    else:
        color("Error: invalid command!", 0)
