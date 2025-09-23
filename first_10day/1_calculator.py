msg = [ "To use the calculator:",
	"Please maintain input method and follow instruction given below – ",
	"[1]For Sumation : `sum 1st 2nd` --> 1st + 2nd",
	"[2]For Abstraction: `abs 1st 2nd` --> 1st - 2nd",
	"[3]For Multiplication: `mult 1st 2nd` --> 1st x 2nd",
	"[4]For Divide: `div 1st 2nd` --> 1st / 2nd",
	"[5]For SqurerootOf: `sqrt X` --> √X",
	"[6]For SqureOf: `sqx X` --> X²"
	]

rest = "\033[0m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
magenta = "\033[95m"

for i in msg:
  print(yellow + i + rest)

print("____________________________________\n")

while True:
  op = input(f"{magenta}Enter operation with proper method:  {rest}")
  op = op.lower()
  if op == "exit" or op == "q":
    print(f"{yellow}Thanks for using calculator :){rest}")
    exit()
  elif "sum" in op.split(" "):
    x, y, z = op.split(" ")
    res = int(y) + int(z)
    print(f"{green}{res}{rest}")

  elif "abs" in op.split(" "):
    x, y, z = op.split(" ")
    res = int(y) - int(z)
    print(f"{green}{res}{rest}")

  elif "mult" in op.split(" "):
    x, y, z = op.split(" ")
    res = int(y) * int(z)
    print(f"{green}{res}{rest}")

  elif "div" in op.split(" "):
    x, y, z = op.split(" ")
    res = int(y) / int(z)
    print(f"{green}{res}{rest}")

  elif "sqx" in op.split(" "):
    x, y= op.split(" ")
    res = int(y) ** 2
    print(f"{green}{res}{rest}")

  else:
    print(f"{red}Error: incorrect input!{rest}")
