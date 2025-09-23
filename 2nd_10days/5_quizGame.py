import json
import time
import colors as c

# Used Variables
score = 0


# Load the quiz file
with open("quiz.json", "r") as f:
  quizzes = json.load(f)

#Game logic and Loop through each quiz

def the_end():
  c.color(f"Your score: {score}/20\n\n________Thank You________\n")
  exit()

def game():
  i = 3
  global score
  real = quiz['answer']
  while i > 0:
    ans = input(f">>Ans: ").lower()
    if ans == "hint":
      i = 2
      show_opt()
    elif ans == "q":
      the_end()
    elif ans == real.lower():
      score += 1
      c.color("Correct! ", 1)
      break
    else:
      c.color(f"Wrong ans, attempts left: {i}\ntype hint for help or q to exit.", 0)
    i -= 1

def show_opt():
  for i, option in enumerate(quiz['options'], start=1):
    print(f"   {i}. {option}")



for quiz in quizzes:
  print(f">>Q{quiz['id']}: {quiz['question']}")
  game()
  if quiz['id'] == 20:
    the_end()



"""    for i, option in enumerate(quiz['options'], start=1):
        print(f"   {i}. {option}")
    print(f"Answer: {quiz['answer']}\n")
"""
