import random, os
import time

rest = "\033[0m"
colors = [
	"\033[91m",
	"\033[92m",
	"\033[93m",
	"\033[94m",
	"\033[95m",
	"\033[96m"
	]



#for i in range(10):
 # clr = random.choice(colors)
  #print(f"{clr}Countdown: {rest}")
#  print(f"{clr}{i}{rest}")
 # time.sleep(1)

#print("")

#n = 10

#while n >= 0:
 # clr = random.choice(colors)
#  print(f"{clr}Countdown: {rest}")
 # print(f"{clr}{n}{rest}")
#  n = n - 1
 # time.sleep(1)



def clear_screen(clr):


  """Clears the terminal screen based on the operating system."""
  # For Windows
  if os.name == 'nt':
      _ = os.system('cls')
  # For macOS and Linux
  else:
      _ = os.system('clear')

def colorText(color, text, rest):
  print(f"{color}{text}{rest}")


x = random.randint(1, 9999)

while x >= 0:
  clr = random.choice(colors)
  clear_screen(clr)
  colorText(clr, f"{x}s", rest)
  time.sleep(1)
  x -= 1

clr = random.choice(colors)
colorText(clr, "Congratulation on end of the countdown!", rest )

