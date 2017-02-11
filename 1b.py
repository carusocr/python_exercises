# Compute whether the given year is a leap year.

###################################################
# Is leapyear formula
# Student should enter function on the next lines.
def is_leap_year(year):
  """
  Returns whether the given Gregorian year is a leap year.
  """ 
  return ((year % 4) == 0 and ((year % 100) != 0 or (year % 400) == 0))


###################################################
# Tests
# Student should not change this code.

def test(year):
  """Tests the is_leapyear function."""
  if is_leap_year(year):
    print year, "is a leap year."
  else:
    print year, "is not a leap year."

test(2000)
test(1996)
test(1800)
test(2013)

###################################################
# Expected output
# Student should look at the following comments and compare to printed output.

#2000 is a leap year.
#1996 is a leap year.
#1800 is not a leap year.
#2013 is not a leap year.

# Compute whether two intervals intersect.

###################################################
# Interval intersection formula
# Student should enter function on the next lines.

def interval_intersect(a,b,c,d):
    return (c <= b and d >= a) or (d <= a and c >= a)

###################################################
# Tests
# Student should not change this code.

def test(a, b, c, d):
    """Tests the interval_intersect function."""
    print "Intervals [" + str(a) + ", " + str(b) + "] and [" + str(c) + ", " + str(d) + "]",
    if interval_intersect(a, b, c, d):
        print "intersect."
    else:
        print "do not intersect."

test(0, 1, 1, 2)
test(1, 2, 0, 1)
test(0, 1, 2, 3)
test(2, 3, 0, 1)
test(0, 3, 1, 2)


###################################################
# Expected output
# Student should look at the following comments and compare to printed output.

#Intervals [0, 1] and [1, 2] intersect.
#Intervals [1, 2] and [0, 1] intersect.
#Intervals [0, 1] and [2, 3] do not intersect.
#Intervals [2, 3] and [0, 1] do not intersect.
#Intervals [0, 3] and [1, 2] intersect.
# Compute a (simplified) Pig Latin version of a word.

###################################################
# Pig Latin formula
def pig_latin(word):
    """Returns the (simplified) Pig Latin version of the word."""
    
    first_letter = word[0]
    rest_of_word = word[1 : ]
    
    # Student should complete function on the next lines.
    v = ['a','e','i','o','u','y']
    if first_letter in v:
        return word + "way"
    else:
        return rest_of_word + first_letter + "ay"


###################################################
# Tests
# Student should not change this code.

def test(word):
    """Tests the pig_latin function."""
    
    print pig_latin(word)
    
test("pig")
test("owl")
test("python")


###################################################
# Expected output
# Student should look at the following comments and compare to printed output.

#igpay
#owlway
#ythonpay
# Compute the smaller root of a quadratic equation.

###################################################
# Smaller quadratic root formula
# Student should enter function on the next lines.

def smaller_root(a,b,c):
    discriminant = b**2 - (4 * a * c)
    if discriminant < 0:
        print "Error: no real solutions"
        return
    if discriminant == 0:
        return -b/2*a
    if discriminant > 0:
        return min(((-b+(discriminant**0.5)))/(2*a),((-b-(discriminant**0.5)))/(2*a))
        

###################################################
# Tests
# Student should not change this code.

def test(a, b, c):
    """Tests the smaller_root function."""
    
    print "The smaller root of " + str(a) + "x^2 + " + str(b) + "x + " + str(c) + " is:" 
    print str(smaller_root(a, b, c))
        

test(1, 2, 3)
test(2, 0, -10)
test(6, -3, 5)

###################################################
# Expected output
# Student should look at the following comments and compare to printed output.

#The smaller root of 1x^2 + 2x + 3 is:
#Error: No real solutions
#None
#The smaller root of 2x^2 + 0x + -10 is:
#-2.2360679775
#The smaller root of 6x^2 + -3x + 5 is:
#Error: No real solutions
#None

#Write a function that calculates the area of a regular polygon, 
#given the number of sides and length of each side. 
#Submit the area of a regular polygon with 7 sides each of length 3 inches. 
#Enter a number (and not the units) with at least four digits
#of precision after the decimal point.
import math
def polyarea(sides,length):
    return (sides*length**2) / (4 * (math.tan(math.pi/sides)))

print polyarea(7,3)
print polyarea(5,7)
----MINI PROJECT
# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
import random
def name_to_number(name):
    # delete the following pass statement and fill in your code below
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    else:
        return 4

def number_to_name(number):
    # delete the following pass statement and fill in your code below
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    else:
        return 'scissors'
    
def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print

    # print out the message for the player's choice
    print "Player chooses " + player_choice

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print "Computer chooses " + comp_choice

    # compute difference of comp_number and player_number modulo five
    difference = (comp_number - player_number) % 5
    # use if/elif/else to determine winner, print winner message
    if difference == 0:
        print "Player and computer tie!"
    elif difference > 2:
        print "Player wins!"
    else:
        print "Computer wins!"
            
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
