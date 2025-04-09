from functools import reduce

# Math Operators
print((2 + 3) * 6)  # 30
print(2 + 3 * 6)  # 20
print(2**8)  # 256  (exponentiation)

print((2 + 3) * 6)  # 30
print(23 // 7)  # 3 (integer division)
print(23 % 7)  # 2 (modulus)


# comments

# Single line comment
# This is a single line comment

# Multi-line comment
"""
This is a multi-line comment
This is a multi-line comment
"""


# Variables
# Variables can even change type after they have been set.
x = 5
x = "Hello"
print(x)  # Hello

# Type Casting
a = int(5)  # int
b = float(5)  # float
c = str(5)  # string
print(type(a))  # 5
print(type(b))  # 5.0
print(type(c))  # 5
# String Formatting
name = "John"
age = 30
# f-string formatting
print(f"My name is {name} and I am {age} years old.")

# Python Keywords (33 keywords)
# as ----->	To create an alias
# assert ----->	For debugging
# break ----->	To break out of a loop
# class ----->	To define a class
# continue ----->	To continue to the next iteration of a loop
# def ----->	To define a function
# del ----->	To delete an object
# elif ----->	Used in conditional statements, same as else if
# else ----->	Used in conditional statements
# except ----->	Used with exceptions, what to do when an exception occurs
# False	Boolean -----> value, result of comparison operations
# finally ----->	Used with exceptions, a block of code that will be executed no matter if there is an exception or not
# for ----->	To create a for loop
# from ----->	To import specific parts of a module
# global ----->	To declare a global variable
# if ----->	To make a conditional statement
# import ----->	To import a module
# in ----->	To check if a value is present in a list, tuple, etc.
# is ----->	To test if two variables are equal
# lambda ----->	To create an anonymous function
# None ----->	Represents a null value
# nonlocal ----->	To declare a non-local variable
# not ----->	A logical operator
# or ----->	A logical operator
# pass ----->	A null statement, a statement that will do nothing
# raise ----->	To raise an exception
# return ----->	To exit a function and return a value
# True ----->	Boolean value, result of comparison operations
# try ----->	To make a try...except statement
# while ----->	To create a while loop
# with ----->	Used to simplify exception handling
# yield ----->	To return a list of values from a generator




# Print even no from 0-20
def find_even_num(num: int):
    even = []
    for value in range(num+1):
        if value%2==0:
            even.append(value)
    return even


print(find_even_num(20))

# sum of all numbers
def sum_all_nums(*nums):
    total  = 0
    for n in nums:
        total +=n
    return total

print(sum_all_nums(2,4,5,6,7,8,3,1))


# Use Reduce to find of all nums
def sum_all_nums_with_reduce(numbers:list):
    total= reduce(lambda acc, current: acc+current, numbers,0)
    return total

print(sum_all_nums_with_reduce([2,4,5,6,7,8,3,1]))
