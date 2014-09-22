import math
import time

wwidth = 1280
wheight = 720

def cache_references(_player, _bullet_array, _enemy_array):
    global player, bullet_array, enemy_array
    player = _player
    bullet_array = _bullet_array
    enemy_array = _enemy_array

class Bullet:
    """BULLETS YO"""
    def __init__(self, x, y, speed, direction, radius, player_owned):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.killyourself = False
        self.player_owned = player_owned
    def move(self):
        self.x = self.x + self.speed*math.cos(self.direction) #wahoo trig
        self.y = self.y + self.speed*math.sin(self.direction)
        if(self.x < 0 or self.y < 0 or self.x > 1280 or self.y > 720):
            self.killyourself = True
    def hitcheck(self):
        if(self.player_owned):
            for enemy in enemy_array:
                safe = self.radius + enemy.radius
                if(safe > abs(self.x - enemy.x)):     #preliminary, hopefully less expensive tests
                    if(safe > abs(self.y - enemy.y)): #to try to reduce computation
                        if(safe > math.sqrt((self.x - enemy.x) * (self.x - enemy.x) + (self.y - enemy.y) * (self.y - enemy.y))): #proper hitcheck
                            enemy.health = enemy.health - 1
                            self.killyourself = True
        else: 
            safe = self.radius + player.radius
            if(safe > abs(self.x - player.x)):     #preliminary, hopefully less expensive tests
                if(safe > abs(self.y - player.y)): #to try to reduce computation
                    if(safe > math.sqrt((self.x - player.x) * (self.x - player.x) + (self.y - player.y) * (self.y - player.y))): #proper hitcheck
                        player.killyourself()
                        self.killyourself = True

class Player:
    """YOU, DAWG"""
    def __init__(self, lives):
        self.lives = lives
        self.x = wwidth/2 #placeholder for center bottom of screen
        self.y = 30 #player always spawns in same place
        self.radius = 1 #hitbox size
        self.speed = 400/60
    def killyourself(self):
        self.lives = self.lives - 1
        if(self.lives < 0):
            game_over()
        else:
            self.x = 0
            self.y = 0
    def moveleft(self):
        if self.x>10:
            self.x =self.x-self.speed
    def moveright(self):
        if self.x<wwidth-10:
            self.x =self.x+self.speed
    def moveup(self):
        if self.y<wheight-10:
            self.y =self.y+self.speed
    def movedown(self):
        if self.y>10:
            self.y =self.y-self.speed  
    def fire(self):
        bullet_array.append(Bullet(self.x, self.y, 5, math.pi/2 , 1, True))
        
class Enemy:
    """THEM"""
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.circular = False
        self.ccw = True #default to counter-clockwise circular motion
        self.speed = 200/60
        self.cx = 0 #circle centre
        self.cy = 0
        self.radius = 1 #hitbox
        self.c_radius = 0 #circular movement radius
        self.killyourself = False
        self.direction = 0 
        self.cool_down_start = 0 #time value
        self.cool_down = 2000 #msec
        self.bullet_count = 0
    def bullet_gen(self): #instantiate a bullet and place it in the active array
        if (time.time()-self.cool_down_start)>self.cool_down:
            if self.bullet_count <10:
                bullet_array.append(Bullet(self.x, self.y, 1, math.atan2((player.y-self.y),(player.x-self.x)), 1, False))
                self.bullet_count = self.bullet_count+1
            else:
                self.cool_down_start = time.time()
                self.bullet_count = 0
    def move(self): #movement
        if(self.circular == True):
            self.direction =  math.atan2((self.y-self.cy)/(self.x-self.cx))
            if(self.ccw == True):
                self.x = self.x + self.speed*math.cos(self.direction+math.pi/2)
                self.y = self.y + self.speed*math.sin(self.direction+math.pi/2)
            else:
                self.x = self.x + self.speed*math.cos(self.direction-math.pi/2)
                self.y = self.y + self.speed*math.sin(self.direction-math.pi/2)
        else:
            self.x = self.x + self.speed*math.cos(self.direction)
            self.y = self.y + self.speed*math.sin(self.direction)
        if(self.x < 0 or self.y < 0 or self.x > 1280 or self.y > 720 or self.health <= 0):
            self.killyourself = True
    def circ(self, cx, cy):
        self.circular = True
        self.cx = 0
        self.cy = 0
        self.c_radius =  math.sqrt((x-cx)*(x-cx) + (y-cy)*(y-cy))
    def line(self, direction):
        self.direction = direction
        self.circular = False
