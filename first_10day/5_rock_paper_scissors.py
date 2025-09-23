import random

print(f"Welcome to Rock, Paper, Scissors game! _/\\_\n")
name = input("Enter your name:  ")

if name.strip() == "":
    print("Please enter your name!")
    exit()
else:
    print(f"Hello, {name}! Please read the instructions below!")

msg = [
    "This is a simple CLI game for you...",
    "Have fun :) Good luck!",
    "Now you will be asked for your choice.\nChoose one of the options between 'R', 'P' and 'S' where -\nR --> Rock\nP --> Paper\nS --> Scissors\n"
]

for i in msg:
    print(f"\033[93m{i}\033[0m")


# Global scores
yscore = 0
cscore = 0

def play_round():
    global yscore, cscore

    options = {"R": "rock", "P": "paper", "S": "scissors"}

    com_opt = random.choice(list(options.values()))
    ut = input("Enter your choice (R, P, S):  ").upper()

    if ut not in options:
        print("Error: Invalid option!")
        return

    user_opt = options[ut]

    print(f"You chose: {user_opt}")
    print(f"Computer chose: {com_opt}")

    # Game logic
    if com_opt == user_opt:
        print("Draw!")
    elif (
        (user_opt == "rock" and com_opt == "scissors") or
        (user_opt == "paper" and com_opt == "rock") or
        (user_opt == "scissors" and com_opt == "paper")
    ):
        yscore += 1
        print(f" You win this round! Your Score: {yscore}")
    else:
        cscore += 1
        print(f" Computer wins this round! Computer Score: {cscore}")


for i in range(7):
    print(f"\n--- Round {i+1} ---")
    play_round()

print("\n====== Final Result ======")
if yscore > cscore:
    print(f"{name.upper()}, you did it! \nFinal Score: You {yscore} - Computer {cscore}")
elif yscore < cscore:
    print(f"Computer wins! Better luck next time... \nFinal Score: You {yscore} - Computer {cscore}")
else:
    print(f"It's a tie! \nFinal Score: You {yscore} - Computer {cscore}")
