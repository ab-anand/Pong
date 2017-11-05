# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [300,200]
ball_vel = [0, 0]
paddle1_pos = 120
paddle2_pos = 120
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel# these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == 'RIGHT':
        ball_vel[0] = random.randrange(3, 5)
        ball_vel[1] = random.randrange(2, 4)
        ball_vel[0] = ball_vel[0]*1
        ball_vel[1] = ball_vel[1]*(-1)
    elif direction == 'LEFT':
        ball_vel[0] = random.randrange(3, 5)
        ball_vel[1] = random.randrange(2, 4)
        ball_vel[0] = ball_vel[0]*(-1)
        ball_vel[1] = ball_vel[1]*(-1)
    else:
        ball_vel[0] = 0
        ball_vel[1] = 1
    new_game()
        
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    #spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle1_vel, paddle2_vel, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
    if ball_pos[1] >= HEIGHT - 20 or ball_pos[1] <= 20:
        ball_vel[1] = ball_vel[1]*(-1)
         
        
    # draw ball
    canvas.draw_circle(ball_pos, 20, 5, 'white', 'white')
    
    # update paddle's vertical position, keep padd-le on the screen
    if paddle1_pos <= 320 :
        if paddle1_vel > 0:
            paddle1_pos += paddle1_vel
    if paddle1_pos >= 0:
        if paddle1_vel < 0:
            paddle1_pos += paddle1_vel
    if paddle2_pos <= 320 :
        if paddle2_vel > 0:
            paddle2_pos += paddle2_vel
    if paddle2_pos >= 0:
        if paddle2_vel < 0:
            paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line([0, paddle1_pos], [0, paddle1_pos+90], 18, 'red')
    canvas.draw_line([600, paddle2_pos], [600, paddle2_pos+90], 18, 'blue')
    
    # determine whether paddle and ball collide    
    if ball_pos[0] <= 28:
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= (paddle1_pos + 90):
            ball_vel[0] = ball_vel[0]*(-1)
            ball_vel[0] += (0.1)*ball_vel[0]
            ball_vel[1] += (0.1)*ball_vel[1]
        else:
            score2 += 1
            spawn_ball('RIGHT')
            
    if ball_pos[0] >= 572:
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= (paddle2_pos + 90):
            ball_vel[0] = ball_vel[0]*(-1)  
            ball_vel[0] +=  (0.1)*ball_vel[0]
            ball_vel[1] +=  (0.1)*ball_vel[1]
        else:
            score1 += 1
            spawn_ball('LEFT')             
        
    # draw scores
    canvas.draw_text(str(score1), (200, 40), 40, 'white')
    canvas.draw_text(str(score2), (400, 40), 40, 'white')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 4
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -4
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 4
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
      
def restart():
    global score1, score2
    score1 = 0
    score2 = 0
    spawn_ball('RIGHT')

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart = frame.add_button('Play!', restart, 100)
label = frame.add_label('Label')
label.set_text('Red paddle - "w" & "s" keys, Blue Paddle - "Up" & "Down"')
# start frame
new_game()
frame.start()
