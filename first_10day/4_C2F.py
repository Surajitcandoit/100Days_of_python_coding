def convert2F():
  Cels = int(input(f"\nEnter celcius value of temparature to convert into Farenhite:  "))

  Far = ((9/5) * Cels) + 32
  peakFar = 1.47 * (10 ** 32)

  if Far > peakFar:
    print(f"\033[91mError: Farenhite value reached out his peak value.. Try lower one!\033[0m\n")
  else:
    print(f"\033[93mFarenhite value is: {Far}\033[0m\n")
convert2F()

while True:
  option = input(f"Want to start over -- type `Y`\nOtherwise 'q' to exit\nOption::  ").lower()

  if option == 'q':
    exit()
  elif option == 'y':
    convert2F()
  else:
    print(f"\033[91mError: incorrect input value\033[0m\n")
