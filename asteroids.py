# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(ship_image, [135,45], ship_info.get_size(), self.pos, ship_info.get_size(),self.angle+self.angle_vel)
        else:
            canvas.draw_image(ship_image, ship_info.get_center(), ship_info.get_size(), self.pos, ship_info.get_size(),self.angle+self.angle_vel)

    def update(self):
        # update ship's angle based on angle_vel
        self.angle += self.angle_vel
        # update ship's position based on velocity
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        forward_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += 0.15 * forward_vector[0]
            self.vel[1] += 0.15 * forward_vector[1]
        # friction
        self.vel[0] *= (0.975)
        self.vel[1] *= (0.975)
        #self.vel[0] 
        
    def inc_angvel(self):
        self.angle_vel += 0.15
        
    def dec_angvel(self):
        self.angle_vel -= 0.15
        
    def shoot(self):
        """
        The missile's initial position should be the tip of your ship's "cannon".
        Its velocity should be the sum of the ship's velocity and a multiple
        of the ship's forward vector.
        def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        """
        global a_missile
        m_vel = [0,0]
        m_vel[0] = angle_to_vector(self.angle)[0]*8 + (self.vel[0]/1.5)
        m_vel[1] = angle_to_vector(self.angle)[1]*8 + (self.vel[1]/1.5)
        a_missile = Sprite([self.pos[0] + self.radius * angle_to_vector(self.angle)[0], self.pos[1]+ self.radius * angle_to_vector(self.angle)[1]], m_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        # update ship's position based on velocity
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age > self.lifespan:
            return True
        return False
        
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) < (self.radius + other_object.radius):
            return True
        return False

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
           
def draw(canvas):
    global time, lives, score, started
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives: " + str(lives), (20,20), 18, "White")
    canvas.draw_text("Score: " + str(score), (WIDTH-140,20), 18, "White")
    
    # draw ship
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    
    # ship hit any rocks?
    if group_collide(rock_group, my_ship):
        lives -= 1
        if lives <= 0:
            started = False
            rock_group.difference_update(rock_group)
            my_ship.draw(canvas)

        
    # missiles hit any rocks? 
    score += group_group_collide(missile_group, rock_group)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    if not started:
        return
    # generate a new asteroid each second. Randomly choose velocity,
    # position, and angular velocity
    # limit asteroids to 12 max
    # add checker to prevent spawning on ship!
    vel1 = random.randrange(5) * random.choice([-1,1])
    vel2 = random.randrange(5) * random.choice([-1,1])
    ang_vel = random.randrange(10)
    pos1 = random.randrange(HEIGHT)
    pos2 = random.randrange(WIDTH)
    if len(rock_group) <= 12:
        a_rock = Sprite([pos1, pos2], [vel1, vel2], 0, 0.07*random.choice([-1,1]), asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        
def process_sprite_group(sprite_group, canvas):
    # helper function to process sprites
    remove_set = set()
    for sprite in sprite_group:
        sprite.draw(canvas)
        if sprite.update():
            remove_set.add(sprite)
    sprite_group.difference_update(remove_set)
                    
def group_collide(sprite_group, other_object):
    # check if any object in group collide with other object
    global lives, score
    remove_set = set()
    for sprite in sprite_group:
        if sprite.collide(other_object):
            remove_set.add(sprite)
    sprite_group.difference_update(remove_set)
    return len(remove_set) != 0
    
def group_group_collide(g1, g2):
    #return the number of elements in the first group that 
    #collide with the second group as well as delete these elements
    #in the first group
    first_group = set(g1)
    collisions = 0
    hits = set()
    for sprite in first_group:
        if group_collide(g2, sprite):
            hits.add(sprite)
            collisions+=1
    g1.difference_update(hits)
    return collisions
        
def keydown(key):
    vel = 0.1
    if key == simplegui.KEY_MAP['left']:
        my_ship.dec_angvel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.inc_angvel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        ship_thrust_sound.play()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()

# register handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

