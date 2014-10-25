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
    __slots__ = ['x','y','speed','direction','radius','killyourself','player_owned']
    
    def __init__(self, x, y, speed, direction, radius, player_owned):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.killyourself = False
        self.player_owned = player_owned
    def move(self,time):
        self.x += self.speed*math.cos(self.direction)*time #wahoo trig
        self.y += self.speed*math.sin(self.direction)*time
        if(self.x < -100 or self.y < -100 or self.x > 1380 or self.y > 820):
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
                            player.power = player.power + 0.5
        else: 
            if player.bomb_state:
                safe = self.radius + player.bomb_radius
                if(safe > abs(self.x - player.bomb_x)):    #BOMB HITCHECK
                    if(safe > abs(self.y - player.bomb_y)): 
                        if(safe > math.sqrt((self.x - player.bomb_x) * (self.x - player.bomb_x) + (self.y - player.bomb_y) * (self.y - player.bomb_y))): 
                            self.killyourself = True
            safe = self.radius + player.radius
            if(safe > abs(self.x - player.x)):     #preliminary, hopefully less expensive tests
                if(safe > abs(self.y - player.y)): #to try to reduce computation
                    if(safe > math.sqrt((self.x - player.x) * (self.x - player.x) + (self.y - player.y) * (self.y - player.y))): #proper hitcheck
                        if player.invuln_time == 0:
                            player.killyourself()
                        self.killyourself = True

class HBullet (Bullet):
    """HOMES, HOMES"""
    
    def move (self, time):
        if(not self.player_owned):
            #NO PLAYER HOMING FUNCTIONALITY FOR NOW
            
            self.direction = math.atan2 (math.sin(self.direction)+(player.y-self.y)/5000, math.cos(self.direction)+(player.x-self.x)/5000)
            #if(math.atan2((player.y-self.y),(player.x-self.x)) - self.direction > math.pi/50):
            #    self.direction = self.direction + math.pi/50
            #elif(self.direction - math.atan2((player.y-self.y),(player.x-self.x)) > math.pi/50):
            #    self.direction = self.direction - math.pi/50
            #else:
            #    self.direction = math.atan2((player.y-self.y),(player.x-self.x))
            #self.direction = math.atan2((player.y-self.y),(player.x-self.x)) -math.pi/3*math.exp(-1*pow(math.hypot(self.x-player.x, self.y-player.y),2))+math.pi/3
            self.speed = self.speed+0.25
            #-45e^(-x)+45
        Bullet.move(self, time)

class TBullet (Bullet):
    """THE T STANDS FOR 'TRIPPING'"""
    
    def move (self, time):
        if(not self.player_owned):
            #I DON'T EVEN KNOW WHY IT DOES THIS
            self.direction = self.direction + (math.atan2((player.y-self.y),(player.x-self.x))) / 120
            #self.direction = self.direction + (math.atan2((player.y-self.y),(player.x-self.x)) - self.direction)/ math.hypot(self.x-player.x, self.y-player.y)
        Bullet.move(self, time)
    

class Player:
    """YOU, DAWG"""
    __slots__ = ['lives','bombs','x','y','radius','speed','last_bullet_fired_time','consecutive_cool_down',\
                 'last_bomb_time','bomb_cool_down','bomb_state','bomb_radius','bomb_x','bomb_y','power','invuln_time']
                 
    def __init__(self, lives, bombs):
        self.lives = lives #extra life
        self.bombs = bombs #droppin bombs
        self.x = wwidth/2 #placeholder for center bottom of screen
        self.y = 30 #player always spawns in same place
        self.radius = 2 #hitbox size
        self.speed = 300 #speed in pixel/seconds
        self.last_bullet_fired_time = 0
        self.consecutive_cool_down = 0.15
        self.last_bomb_time = 0
        self.bomb_cool_down = 1
        self.bomb_state = False
        self.bomb_radius = 0
        self.bomb_x = 0
        self.bomb_y = 0
        self.power = 0 #NO ONE MAN SHOULD HAVE ALL THAT POWER
        self.invuln_time = 0
    def killyourself(self):
        self.lives = self.lives - 1
        if(self.lives < 0):
            game_over()
        else:
            self.x = 640
            self.y = 50
            self.invuln_time = 100
    def moveleft(self,time):
        if self.x>10:
            self.x -=self.speed * time
    def moveright(self,time):
        if self.x<wwidth-10:
            self.x +=self.speed * time
    def moveup(self,time):
        if self.y<wheight-10:
            self.y +=self.speed * time
    def movedown(self,time):
        if self.y>10:
            self.y -=self.speed * time
    #def fire(self):
        #bullet_array.append(Bullet(self.x, self.y, 4, math.pi/2 , 1, True))
        #bullet_array.append(Bullet(self.x, self.y, 4, 5*math.pi/12 , 1, True))
        #bullet_array.append(Bullet(self.x, self.y, 4, 7*math.pi/12 , 1, True))
    def fire(self): #instantiate a bullet and place it in the active array            
        if self.power > 4:
            if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                bullet_array.append(Bullet(self.x-10, self.y, 30*60, math.pi/2 , 1, True))
                bullet_array.append(Bullet(self.x+10, self.y, 30*60, math.pi/2 , 1, True))
        if self.power > 3:
            if(time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                bullet_array.append(Bullet(self.x-10, self.y, 15*60, 9*math.pi/24 , 1, True))
                bullet_array.append(Bullet(self.x+10, self.y, 15*60, 15*math.pi/24 , 1, True))
        if self.power > 2:
            if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                bullet_array.append(Bullet(self.x-25, self.y-20, 20*60, math.pi/2 , 1, True))
                bullet_array.append(Bullet(self.x+25, self.y-20, 20*60, math.pi/2 , 1, True))
        if self.power > 1:
            if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                bullet_array.append(Bullet(self.x+5, self.y, 10*60, 5*math.pi/12 , 1, True))
                bullet_array.append(Bullet(self.x-5, self.y, 10*60, 7*math.pi/12 , 1, True))
        if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                bullet_array.append(Bullet(self.x, self.y, 15*60, math.pi/2 , 1, True))
                self.last_bullet_fired_time = time.time()
    def bomb(self):
        if(self.bombs > 0 and (time.time()-self.last_bomb_time)>self.bomb_cool_down):
            self.bombs = self.bombs - 1
            self.last_bomb_time = time.time()
            self.bomb_state = True
            self.bomb_x = self.x
            self.bomb_y = self.y
            self.invuln_time = 100
        
class Enemy:
    """THEM"""
    __slots__ = ['x','y','health','circular','ccw','speed','cx','cy','radius','killyourself','direction','last_bullet_fired_time',\
                 'stream_cool_down','consecutive_cool_down','bullet_count']
    def __init__(self, x, y, health, stream_cool_down = 0, direction = 0, circular = False, ccw = True, cx = 0, cy = 0, speed = 200):
        self.x = x
        self.y = y
        self.health = health
        self.circular = circular
        self.ccw = ccw #default to counter-clockwise circular motion
        self.speed = speed #in pixel/seconds
        self.cx = cx #circle centre
        self.cy = cy
        self.radius = 10 #hitbox
        self.killyourself = False
        self.direction = direction
        self.last_bullet_fired_time = 0
        self.stream_cool_down = stream_cool_down #time value
        self.consecutive_cool_down = 0.05
        self.bullet_count = 10
    def fire(self): #instantiate a bullet and place it in the active array            
        if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
            if self.bullet_count > 0 and time.time() > self.last_bullet_fired_time:
                bullet_array.append(Bullet(self.x, self.y, 180, math.atan2((player.y-self.y),(player.x-self.x)), 1, False))
                self.bullet_count = self.bullet_count-1
                self.last_bullet_fired_time = time.time()
            else:
                self.last_bullet_fired_time = self.stream_cool_down + self.last_bullet_fired_time
                self.bullet_count = 10
    def move(self,time): #movement
        if(self.circular == True):
            self.direction =  math.atan2((self.y-self.cy),(self.x-self.cx))
            if(self.ccw == True):
                self.x += self.speed*math.cos(self.direction+math.pi/2)*time
                self.y += self.speed*math.sin(self.direction+math.pi/2)*time
            else:
                self.x += self.speed*math.cos(self.direction-math.pi/2)*time
                self.y += self.speed*math.sin(self.direction-math.pi/2)*time
        else:
            self.x += self.speed*math.cos(self.direction)*time
            self.y += self.speed*math.sin(self.direction)*time
        if(self.x < -50 or self.y < -50 or self.x > 1330 or self.y > 770 or self.health <= 0):
            self.killyourself = True
    def circ(self, cx, cy):
        self.circular = True
        self.cx = cx
        self.cy = cy
    def line(self, direction):
        self.direction = direction
        self.circular = False

class StageOneBoss (Enemy):
    def __init__(self):
        Enemy.__init__(self, 0,0,0,0)
        self.x = 640
        self.y = 360
        self.health = 5000
        self.speed = 0
        self.radius = 100
        self.stream_cool_down = 2
        self.bullet_count = 100
        self.power = 0
    def fire(self): #instantiate a bullet and place it in the active array
        self.power = (5000 - self.health)/500
        if self.power > 7:
            if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                if self.bullet_count > 0 and time.time() > self.last_bullet_fired_time: 
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))-2*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))+2*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))-3*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))+3*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))-4*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))+4*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))-5*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))+5*math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 4*60, math.atan2((player.y-self.y),(player.x-self.x))-6*math.pi/6 , 1, False))
                    self.bullet_count = self.bullet_count-9
        if self.power > 5:
            if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                if self.bullet_count > 0 and time.time() > self.last_bullet_fired_time:
                    bullet_array.append(Bullet(self.x, self.y, 7*60, math.atan2((player.y-self.y),(player.x-self.x))-math.pi/6 , 1, False))
                    bullet_array.append(Bullet(self.x, self.y, 7*60, math.atan2((player.y-self.y),(player.x-self.x))+math.pi/6 , 1, False))
                    self.bullet_count = self.bullet_count-2
        if self.power > 3:
            if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
                if self.bullet_count > 0 and time.time() > self.last_bullet_fired_time:
                    bullet_array.append(Bullet(self.x-10, self.y, (2+self.power/2)*60, math.atan2((player.y-self.y),(player.x-10-self.x)), 1, False))
                    bullet_array.append(Bullet(self.x+10, self.y, (2+self.power/2)*60, math.atan2((player.y-self.y),(player.x+10-self.x)), 1, False))
                    self.bullet_count = self.bullet_count-2
        if (time.time()-self.last_bullet_fired_time)>self.consecutive_cool_down:
            if self.bullet_count > 0 and time.time() > self.last_bullet_fired_time:
                bullet_array.append(HBullet(self.x, self.y, (2+self.power/2)*60, math.atan2((player.y-self.y),(player.x-self.x)), 1, False))
                self.bullet_count = self.bullet_count-1
                self.last_bullet_fired_time = time.time()
            else:
                self.last_bullet_fired_time = self.stream_cool_down + self.last_bullet_fired_time
                if self.power > 7:
                    self.bullet_count = 5000
                elif self.power > 5:
                    self.bullet_count = 1000
                elif self.power > 3:
                    self.bullet_count = 400
                else:
                    self.bullet_count = 0
                    

class Stage:
    def __init__(self, time_queue, enemy_queue): #stage is not activated until stage_activate(time.time()) called
        self.stage_start_time = 0 # secs
        self.time_queue = time_queue # secs from stage start
        self.enemy_queue = enemy_queue #enemy_queue is array of [x,y,health,stream_cool_down,direction=0,circular=False,cx=0,cy=0]
        self.enemy_count = len(enemy_queue) # total number of enemies
        self.counter = 0
    def stage_activate(self, stage_start_time):
        self.stage_start_time = stage_start_time
    def make_things_appear(self): #method to call every loop() iteration in main to check if things can be added
        while (self.stage_start_time>0 and self.enemy_count > self.counter and time.time() > self.time_queue[self.counter] + self.stage_start_time):
            #enemy_array.append(self.enemy_queue[self.counter])
            enemy_array.append(Enemy(*(self.enemy_queue[self.counter])))
            self.counter = self.counter + 1
