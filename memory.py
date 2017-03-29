# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global state, deck, exposed, first, second, turns
    state = 0
    turns = 0
    deck = [card for card in range(8)]*2
    exposed = [False]*16
    random.shuffle(deck)
    label.set_text("Turns = " + str(turns))


# define event handlers
def mouseclick(pos):
    global exposed, state, first, second, turns
    # add game state logic here
    card_clicked = pos[0]//50
    if state == 0:
        exposed[card_clicked] = True
        first = card_clicked
        state = 1
    elif state == 1:
        if exposed[card_clicked] == False:
            exposed[card_clicked] = True
            second = card_clicked
            state = 2
            turns += 1
    else:
        if exposed[card_clicked] == False:
            exposed[card_clicked] = True
            if deck[first] == deck[second]:
                pass
            else:
                exposed[first] = False
                exposed[second] = False
            exposed[card_clicked] = True
            first = card_clicked
            state = 1
    label.set_text("Turns = " + str(turns))
        

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck, exposed
    for i in range(16):
        if exposed[i] == True:
            canvas.draw_text(str(deck[i]), ((20+50*i),60),24,'White')
        else:
            canvas.draw_polygon([(0+i*50,0),(50+i*50,0),
                                 (50+i*50,100),(0+i*50,100)],
                                2,"Yellow","Green")
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
