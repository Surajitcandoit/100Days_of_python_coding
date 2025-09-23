print("Hello World!")
#this is a comment line syntax --> #
"""
this a multi line 
comment as you 
see here!

"""

#python variable
var_name = "value" #syntax to create a variable 

#example
name = "hacker"
nem = 23

"""
key note: 
1. variable name cannot be started with an integer(1,2,3) or an special characters(eg- #,$,@)

2. in python variable name is very case sensitive means that Var_name ≠ var_name

3. don't contains spaces in variable name 
"""

"""
Data types
data: basically a value that we are stored into a variable 

1.Strings -- "Alex", "Hello"
2.Integer -- 12, -6, 3527
3.Float -- 1.2, 3.14, -2.3
4.Boolean -- True, False
5.Set -- {1,2,"hi","apple",True}
6.List -- [8,"alex","python",True]
7.Tuple -- (3,4,6,7,"kiwi")
8.Dictionary -- {"key": "value", "name": "alex"}
9.Complex -- (x + iy)
10.None -- None
"""

message= "Hi everyone"  
# ⁰H¹i² ³e⁴v⁵e⁶r⁷y⁸o⁹n¹⁰e¹¹
print(message) #output --> Hi everyone
print(message[0]) #output --> H
#indexing: just like numbering but start from 0

#slicing
x = message[:2] 
#index [0 to 2) 
#lower_index = 0 but upper_index < 2

y = message[3:6]
print(x) #output --> Hi
print(y) #output --> eve


k = "Alex"
l = "Paro"
m = f"{k} {l}"
print(m) #Alex Paro

#operators
a = 9
b = 2

print(a+b) #11
print(a-b) #7

"""
similarly 
a*b = 9 x 2 multiplication 
a/b = 9 / 2 division(➗)
a%b = 1 reminder
a**b = a to the power b
a**2 = a²

a=b -- False
a!=b -- True
less than <
greater than >
less than equal to <=
greater than equal to >=

and -- True if both are true.
or -- True if any statement is true. False when both false

not -- reverse the equation or condition 

...
...
"""

a = 6
b = 3

if a == b: #False → then skip the if block.
  print("no way!")
else:
  print("👍")

#output --> 👍 


if a > b:
  print("a greter than b")
elif a < b:
  print("a less than b")
else:
  print("a equal to b")

#output --> a greater than b

for i in range(10):
  print(i)

"""
output:
1
2
3
4
5
6
7
8
9
10
"""
for char in "Hello":
  print(char)
"""
output:
H
e
l
l
o
"""
k = 0
while k<4:
  print(k)
  k+=1

"""
output:
0
1
2
3
4
"""

for i in range(5):
  if i == 3:
    break #continue
  print(i)

k = 0
while True:
  if k == 3:
    break 
  print(k)
  k+=1

"""
output:
1
2
"""
age = 17
match age:
  case age>=18:
    print("you are adult")
  case age<18:
    print("you are minor")
  default:
    pass #do nothing, create default as blank

#output: you are minor

my_list = [2,3]
print(my_list[0]) 
#2 print by index→tuple, list

my_list.append(5) #[2,3,5]
my_list.extend([4,1])
my_list.sort()
my_list.remove(4)
my_list.pop()
my_list.clear()

tup = (5,6,8,4,"hi")
tup.count(5)
print(tup[4]) #hi


set1 = {2,4,3}
set2 = {6,4,3,8}
k = set1.union(set2) #set1 + set2
print(k)
k = set2.difference(set1) #set2 - set1
print(k)
#set1.intersection(set2)


dict1 = {
         "name": "alex",
         "age": 18,
         "roll": 21
         }
print(dict1["name"]) #alex


#to create a function→use 'def' keyword 
def greet():
  print("Hi everyone")
greet() #calling the function 
  
#output: Hi everyone 

name = "Kamora"
msg = "How are you?"
def ask():
  print(f"Hi {name}, {msg}") 
ask()

def ask_it(a, b):
  print(f"Hi {a}, {b}")
ask_it(name, msg)
#output: Hi Kamora, How are you?


class Students:
  def __init__(self, name, cls=10):
    self.name = name 
    self.cls = cls
  def show(s):
    print(f"Hi {s.name}.")

s1 = Students("Sunny", 8)
s1.show() #Hi Sunny

