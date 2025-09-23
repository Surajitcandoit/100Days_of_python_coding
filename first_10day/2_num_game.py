import sys, random, time

# Startup messages
msg = ["Loading the game....", "Initializing game...", "Reading game data..."]

for i in msg:
    print(f"\033[92m{i}\033[0m", end="")
    sys.stdout.flush()
    time.sleep(1)
    print("\033[92m Done.\033[0m")

print("_____________________________________\n")
print(f"\033[95mWelcome to the Guessing Game Arcade!\033[0m")


name = input("Enter your name:  ").strip()

while not name:
    print(f"\033[93mPlease enter your name to start the game!\033[0m")
    name = input("Enter your name:  ").strip()


def game():
    print(f"\nHi, {name}! 🎮 This is a number guessing game.")
    print("You have 7 chances to guess the correct number between 1 and 50.\n")

    sec_num = random.randint(1, 50)

    for attempt in range(1, 8):
        try:
            guess_num = int(input(f"Attempts-{attempt}/7 - Enter your guess: "))

            if guess_num == sec_num:
                 print(f"\033[94m🎉 You got it! Boom -- the number is {guess_num}\033[0m\n")
                 break
            elif guess_num < sec_num:
                 print("\033[96mYour guess is too low, try a larger one.\033[0m\n")
            else:
                 print("\033[96mYour guess is too high, try a lower one.\033[0m\n")

        except ValueError:
            print("\033[91mInvalid input! Please enter a number.\033[0m\n")

        if attempt == 7:
            print(f"\033[91mGame Over! You failed to guess it.\nThe number was {sec_num}.\033[0m\n")


if __name__ == "__main__":
    game()
