
# Asteroid
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import simpleguitk as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
GAP = 15
FRICTION = .99
ACCELERATION = .3
MISSILE_SPAWN_DISTANCE = 45
MISSILE_SPEED = 10
ROCK_DISTANCE_LIMIT = 200
ROCK_SPEED = 20
score = 0
lives = 3
time = 0.5
difficulty = float(1)
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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

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
soundtrack = simplegui.load_sound("soundtrack.ogg")
missile_sound = simplegui.load_sound("missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("thrust.ogg")
explosion_sound = simplegui.load_sound("explosion.ogg")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

#instead of using a seperate variable for each result, using modified angle_to_vector-like function, purely for the result of thruster
def thruster(vel,angle):
    return [(vel[0] + ACCELERATION* math.cos(angle)),(vel[1]+ACCELERATION*math.sin(angle))]

#helper function, adds (a,b) to (c,d) or multiplies a and (c,d)
def listmath(first, action, second):
    if action == "*":
        return [(first*second[0]),(first*second[1])]
    elif action == "+":
        return [(first[0]+second[0]),(first[1]+second[1])]

#does world-edge wrapping.  If the ship (or a rock) is close to the edge of the world, calculates where to draw the duplicate objects
def edgecheck(pos,size):
    loc = set([(pos[0],pos[1])])
    if(pos[0] < size):
        loc.add((pos[0]+int(WIDTH+GAP),pos[1]))
        if(pos[1] < size):
            loc.add((pos[0]+int(WIDTH+GAP),pos[1]+int(HEIGHT+GAP)))
        if(pos[1] > HEIGHT - size):
            loc.add((pos[0]+int(WIDTH+GAP),pos[1]+int(-HEIGHT-GAP)))
    
    if(pos[1] < size):
        loc.add((pos[0],pos[1]+int(HEIGHT+GAP)))
    if(pos[1] > HEIGHT-size):
        loc.add((pos[0],pos[1]+int(-HEIGHT-GAP)))

    if(pos[0] > (WIDTH - size)):
        loc.add((pos[0]+int(-WIDTH-GAP),pos[1]))
        if(pos[1] < size):
            loc.add((pos[0]+int(-WIDTH-GAP),pos[1]+int(+HEIGHT+GAP)))
        if(pos[1] > HEIGHT - size):
            loc.add((pos[0]+int(-WIDTH-GAP),pos[1]+int(-HEIGHT-GAP)))
    return loc

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

    def get_center(self):
        return self.pos
    def get_radius(self):
        return self.radius
    
    #draw 5 ships, for the sake of edge wrapping and ship being visible through the edge of the world
    def draw(self,canvas):
        locations = edgecheck(self.pos,self.radius)
        for i in locations:
            #thruster image modification happens by adding self.thrust which is 1 or 0 multipled by self.image_size[0]
            canvas.draw_image(self.image, (self.image_center[0]+self.thrust*self.image_size[0],self.image_center[1]), self.image_size, i, self.image_size, self.angle)

    def update(self):
        #rotate if called to
        self.angle+=self.angle_vel

        #thruster sound
        if self.thrust:
            ship_thrust_sound.play()
            self.vel = thruster(self.vel,self.angle)
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()


        #movement/friction
        self.pos = listmath(self.vel,"+",self.pos)
        self.vel = listmath(FRICTION,"*",self.vel)
        
        #edge-wrapping
        if self.pos[0] < -GAP:
            self.pos[0] = WIDTH
        if self.pos[0] > WIDTH:
            self.pos[0] = -GAP
        if self.pos[1] < -GAP:
            self.pos[1] = HEIGHT
        if self.pos[1] > HEIGHT:
            self.pos[1] = -GAP

    def shoot(self):
        missile_group.add(Sprite(listmath(self.pos,"+",listmath(MISSILE_SPAWN_DISTANCE,"*",angle_to_vector(self.angle))),listmath(listmath(MISSILE_SPEED,"*",angle_to_vector(self.angle)),"+",self.vel), self.angle, 0, missile_image, missile_info, missile_sound))
        
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
    def get_image(self):
        return self.animated
    def get_center(self):
        return self.pos
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        #for the sake of edge-wrapping
        locations = edgecheck(self.pos,self.radius)
        #if its animated, uses age value to shift through the image
        for i in locations:
            canvas.draw_image(self.image, (self.image_center[0]+self.animated*self.age*self.image_size[0],self.image_center[1]), self.image_size, i, self.image_size, self.angle)

    def update(self):
        #Spin/move
        self.angle += self.angle_vel
        self.pos = listmath(self.pos,"+",self.vel)
        self.age += 1
        #edge wrap
        if self.pos[0] < -GAP:
            self.pos[0] = WIDTH
        if self.pos[0] > WIDTH:
            self.pos[0] = -GAP
        if self.pos[1] < -GAP:
            self.pos[1] = HEIGHT
        if self.pos[1] > HEIGHT:
            self.pos[1] = -GAP
            
        if self.age > self.lifespan:
            return True
        else:
            return False

    def collide(self, other_object):
        if(dist(self.pos,other_object.get_center()) < (self.radius + other_object.get_radius())):
            #if it hits something, generate a kaboom, and return true to know it needs to be deleted from the list
            explosions_group.add(Sprite(self.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
            return True
        return False
               
        
def process_sprite_groups(canvas, group):
    for item in set(group):
        #draw an item, then a true/false check from update, indicating if an item needs removing
        item.draw(canvas)
        if(item.update()):
            group.remove(item)
        
def group_collide(single, group):
    collisions = 0
    #count collisions, remove object struck from set, return count of how many items struck in the case of multiple simultaneous strikes
    for item in set(group):
        if item.collide(single):
            group.remove(item)
            collisions +=1
    return collisions

def group_group_collide(rocks, missiles):
    points = 0
    #for each missile, check each missile in group_collide to every rock, return the number of hits.
    #using an internally-generated set, so can safely modify the passed set, removing missiles that land a hit, and gives points for each rock struck
    for missile in set(missiles):
        hits = group_collide(missile,rocks)
        if (hits):
            points += hits
            missiles.remove(missile)
    return points

def click(pos):
    global started, lives,score
    #no idea what any of this does, just copied from updated template
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        difficulty = 1
        soundtrack.play()

def draw(canvas):
    global time, score, lives, started, difficulty
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        soundtrack.pause()
        soundtrack.rewind()
    
    # update ship and sprites
    my_ship.update()

    process_sprite_groups(canvas, rock_group)
    process_sprite_groups(canvas, missile_group)
    process_sprite_groups(canvas, explosions_group)

    #missile hitting rocks, gives points, use the group_group function to work out how many
    score += group_group_collide(rock_group,missile_group)
    
    #modified difficulty by increasing potential rock speed
    if (score > 10):
        difficulty = float(int(score-10)/10)/2+1

    if(group_collide(my_ship,rock_group)):
        lives -=1
    if (lives == 0):
        #Game over man, game over.  Remove the remaining rocks, prevent more spawning
        for rock in set(rock_group):
            rock_group.remove(rock)
        started = False

    canvas.draw_text("Lives: "+str(lives),(650,50),30,"Red")
    canvas.draw_text("Score: "+str(score),(50,50),30,"Red")
    
    #display difficulty text, only displays when difficulty has gone up
    if (not difficulty == 1):
        canvas.draw_text("Difficulty: "+str(int(2*(difficulty-1)+1)),(600,100),30,"RED")

#checks distance from potential rock spawn location to ship.  Including distances across the four world-edges.        
#similar code to edge_check, could simplify code in the future
def rock_check(guess):
    ship = my_ship.get_center()
    lowest = dist(ship,guess)
    if ship[0] < ROCK_DISTANCE_LIMIT:
        if dist((WIDTH+GAP+ship[0], ship[1]), guess) < lowest:
            lowest = dist((WIDTH+GAP+ship[0], ship[1]), guess)
        if ship[1] < ROCK_DISTANCE_LIMIT:
            if dist((WIDTH+GAP+ship[0], (HEIGHT-GAP+ship[1])), guess) < lowest:
                lowest = dist((WIDTH-GAP+ship[0], (HEIGHT+GAP+ship[1])), guess)
        if ship[1] > HEIGHT-ROCK_DISTANCE_LIMIT:
            if dist((WIDTH+GAP+ship[0], (ship[1]-HEIGHT-GAP)),guess) < lowest:
                lowest = dist((WIDTH+GAP+ship[0], (ship[1]-HEIGHT-GAP)),guess)

    if ship[0] > WIDTH - ROCK_DISTANCE_LIMIT:
        if dist((ship[0] - WIDTH-GAP, ship[1]), guess) < lowest:
            lowest = dist((ship[0] - WIDTH-GAP, ship[1]), guess)
        if ship[1] < ROCK_DISTANCE_LIMIT:
            if dist((ship[0] - WIDTH-GAP, (HEIGHT+GAP+ship[1])), guess) < lowest:
                lowest = dist((ship[0] - WIDTH-GAP, (HEIGHT+GAP+ship[1])), guess)
        if ship[1] > HEIGHT-ROCK_DISTANCE_LIMIT:
            if dist((ship[0] - WIDTH-GAP, (ship[1]-HEIGHT-GAP)),guess) < lowest:
                lowest = dist((ship[0] - WIDTH-GAP, (ship[1]-HEIGHT-GAP)),guess)

    if ship[1] < ROCK_DISTANCE_LIMIT:
        if dist((ship[0],HEIGHT+GAP+ship[1]),guess) < lowest:
            lowest = dist((ship[0],HEIGHT+GAP+ship[1]),guess)
    if ship[1] > HEIGHT - ROCK_DISTANCE_LIMIT:
        if dist((ship[0],ship[1]-HEIGHT-GAP),guess) < lowest:
            lowest = dist((ship[0],ship[1]-HEIGHT-GAP),guess)
    return lowest

# timer handler that spawns a rock
def rock_spawner():
    global rock_group
    if (len(rock_group) < 12 and started):
        #makes sure rocks dont spawn too close to the ship, based on a global constant
        #rock speed limits modified by difficulty
        #duplicate code for assigning test_pos to a random number, I dont like it, but seems unavoidable for how I have the loop
        test_pos = (random.randrange(0,WIDTH), random.randrange(0,HEIGHT))
        while rock_check(test_pos) < ROCK_DISTANCE_LIMIT:
#            print test_pos," too close to ship ", my_ship.get_center()
            test_pos = (random.randrange(0,WIDTH), random.randrange(0,HEIGHT))
        rock_group.add(Sprite(test_pos, [random.randrange(-ROCK_SPEED*difficulty,ROCK_SPEED*difficulty)/10, random.randrange(-ROCK_SPEED*difficulty,ROCK_SPEED*difficulty)/10], 0, float(random.randrange(-100,100,40))/1000, asteroid_image, asteroid_info))

def keydown(key):
    #theres better ways for this code, may change this later, but its the keyboard input
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = -.1
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = .1
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship, facing vertially, and three empty sprites sets
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 4.712, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosions_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
