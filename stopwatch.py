# template for "Stopwatch: The Game"

import simplegui

# define global variables

t = 0
num_stops = 0
num_hits = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = t // 600
    seconds = t % 600 // 10
    ms = t % 60 % 10
    return "%02d:%02d" % (minutes, seconds) + "." + str(ms)
    
format(661)

def tick():
    global t
    t += 1
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global num_stops, num_hits
    if not timer.is_running():
        return
    timer.stop()
    num_stops += 1
    if t % 10 == 0:
        num_hits +=1

def reset():
    global t, num_stops, num_hits
    t, num_stops, num_hits = 0, 0, 0
    

# define event handler for timer with 0.1 sec interval

timer = simplegui.create_timer(100, tick)

# define draw handler
def draw(canvas):
    canvas.draw_text(format(t),[50,100],32,"Red")
    canvas.draw_text(str(num_hits) + "/" + str(num_stops), [160,20],24,"Green")
    
# create frame
frame = simplegui.create_frame("Exciting Timer!", 200, 200)
frame.set_draw_handler(draw)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)

# register event handlers

# start frame
frame.start()

# Please remember to review the grading rubric
