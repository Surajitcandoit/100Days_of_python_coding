import time, random

dice1 = f"—————————\n|\t|\n|   o   |\n|\t|\n—————————"
dice2 = f"—————————\n| o     |\n|       |\n|     o |\n—————————"
dice3 = f"—————————\n| o     |\n|   o   |\n|     o |\n—————————"
dice4 = f"—————————\n| o   o |\n|       |\n| o   o |\n—————————"
dice5 = f"—————————\n| o   o |\n|   o   |\n| o   o |\n—————————"
dice6 = f"—————————\n| o o o |\n|       |\n| o o o |\n—————————"

dices = [dice1, dice2, dice3, dice4, dice5, dice6]

tr1 = f"————\n|\n|\n|\n————"
tr2 = f"   |\n   |\n   |"
tr3 = f"    ————\n\t|\n\t|\n\t|\n    ————"
tr4 = f"—————————\n|\t|\n|       |\n|\t|\n—————————"

frames = [tr1, tr2, tr3, tr4]

def transition():
  for i in frames:
    print(i)
    time.sleep(0.1)

def rolled():
  print(random.choice(dices))


def roll_thedice():
  #transition()
  rolled()

rolled()


while True:
  n = input("Do you want to roll the dice(y/n): ").lower()
  if n == "y":
    roll_thedice()
  elif n == "n":
    print("As per user operation cancelled!\n\nGame ended, good bye!\n")
    exit()
  else:
    print("error(1): invalid input!")
