# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 14
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
sk = simplegui.KEY_MAP

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(2,4),-random.randrange(1,4)]
    else:
        ball_vel = [-random.randrange(2,4),-random.randrange(1,4)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2 #these are ints
    paddle1_pos, paddle2_pos = (HEIGHT - PAD_HEIGHT)/2, (HEIGHT - PAD_HEIGHT)/2
    paddle1_vel = paddle2_vel = 0
    score1, score2 = 0, 0
    spawn_ball(RIGHT)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball, determine whether paddle and ball collide    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if (paddle1_pos <= ball_pos[1]) and (ball_pos[1] <= (paddle1_pos+PAD_HEIGHT)):
            ball_vel[0]=-1.2*ball_vel[0]
        else:
            spawn_ball(RIGHT)
            score2 += 1
    if ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if (paddle2_pos <= ball_pos[1]) and (ball_pos[1] <= (paddle2_pos+PAD_HEIGHT)):
            ball_vel[0] = - 1.2*ball_vel[0]
        else:
            spawn_ball(LEFT)
            score1 += 1
    #handle vertical hits
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White","White")

    # update paddle's vertical position, ignore command if moves paddle offscreen
    if (paddle1_pos + paddle1_vel) >= 0 and (paddle1_pos + paddle1_vel) <= (HEIGHT - PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel) >= 0 and (paddle2_pos + paddle2_vel) <= (HEIGHT - PAD_HEIGHT):
        paddle2_pos += paddle2_vel   
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos],[HALF_PAD_WIDTH, paddle1_pos+PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos],[WIDTH- HALF_PAD_WIDTH, paddle2_pos+PAD_HEIGHT], PAD_WIDTH, "White")
       
    # draw scores
    canvas.draw_text(str(score1), (40,20), 20, "White")
    canvas.draw_text(str(score2), (550,20), 20, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, sk
    vel = 6
    if key == sk['down']:
        paddle2_vel = vel
    elif key == sk['up']:
        paddle2_vel = -vel
    elif key == sk['x']:
        paddle1_vel = vel
    elif key == sk['w']:
        paddle1_vel = -vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel, sk
    if key == sk['w'] or key == sk['x']:
        paddle1_vel = 0
    elif key == sk['down'] or key == sk['up']:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
