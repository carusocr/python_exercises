# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui

range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global max_guesses
    if range == 100:
        max_guesses = 7
    else:
        max_guesses = 10
    secret_number = random.randrange(0,range)

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range
    range = 100
    print "Starting new game with range [0,100). You get 7 guesses!"
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range
    range = 1000
    print "Starting new game with range [0,1000). You get 10 guesses!"
    new_game()
    
    
def input_guess(guess):
    
    global max_guesses
    print "Guess was " + guess
    guess = int(guess)    
    if guess >= range or guess < 0:
        print "Enter a number between 0 and " + str(range-1) + "!"
        return
    # main game logic goes here 
    if guess > secret_number:
        print "Lower!"
    elif guess < secret_number:
        print "Higher!"
    else:
        print "Correct!"
    max_guesses -= 1
    print "Guesses remaining: " + str(max_guesses)
    if max_guesses == 0:
        print "Out of guesses! Starting new game with range [0," + str(range) + ")."
        new_game()

    
# create frame

frame = simplegui.create_frame("Guess the number.",100,200)
frame.add_input("Enter guess:",input_guess,100)
frame.add_button("Range is [0,100)",range100)
frame.add_button("Range is [0,1000)",range1000)
# register event handlers for control elements and start frame


# call new_game 
print "Starting new game with range [0,100)."
new_game()
frame.start()
