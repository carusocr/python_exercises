### Program structure of event-driven programs:
# declare globals
# helper functions
# classes
# define event handlers
# create a frame
# register event handlers
# start frame and any timers


# Example of a simple event-driven program

# CodeSkulptor GUI module
import simplegui

# Event handler
def tick():
    print "tick!"

# Register handler
timer = simplegui.create_timer(1000, tick)

# Start timer
timer.start()

# SimpleGUI program template

# Import the module
import simplegui

# Define global variables (program state)

ctr=0

# Define "helper" functions

def increment():
    global ctr
    ctr = ctr + 1
    
# Define event handler functions

def tick():
    increment()
    print ctr
    
def buttonpress():
    global ctr
    ctr = 0

# Create a frame

frame = simplegui.create_frame("Zug", 100, 100)
frame.add_button("Zug me!", buttonpress)

# Register event handlers
timer = simplegui.create_timer(1000, tick)

# Start frame and timers
frame.start()
timer.start()

