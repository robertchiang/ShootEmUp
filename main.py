#!/usr/bin/python

import pyglet
from pyglet.window import key
from pyglet.window import mouse
import math
from pyglet.gl import *


import time
import csv
import copy

from classes import *

def import_stage(filename): # format of row: time,x,y,health,stream_cool_down,direction=0,circular=False,cx=0,cy=0
    time_queue = []
    enemy_queue = []
    with open(filename, 'r') as f:
        delimited_text = csv.reader(f, delimiter=',', skipinitialspace=True, quotechar='"')
        for row in delimited_text:
            if row and len(row) > 0 and len(row[0])> 0 and not row[0][0] == "#": #first row is comments, doesnt count
                time_queue.append(float(row[0]))
                enemy_args = [ globals()[(row[1])] ]
                
                #if len(row)>5:
                for i in range(2, len(row)):
                    if len(row[i])>0:
                        if i == 2:      enemy_args.append(int(row[2]))
                        elif i == 3:    enemy_args.append(int(row[3]))
                        elif i == 4:    enemy_args.append(int(row[4]))
                        elif i == 5:    enemy_args.append(float(row[5]))
                        elif i == 6:    enemy_args.append(float(eval(row[6])))
                        elif i == 7:    enemy_args.append(bool(int(row[7])))
                        elif i == 8:    enemy_args.append(bool(int(row[8])))
                        elif i == 9:    enemy_args.append(int(row[9]))
                        elif i == 10:   enemy_args.append(int(row[10]))
                        elif i == 11:   enemy_args.append(int(row[11]))
                enemy_queue.append(enemy_args)
    return Stage(time_queue, enemy_queue)


def load_resources():
    global key_state, key_action_time, mouse_state
    key_state = { key.LEFT: False, key.RIGHT: False, key.UP: False, key.DOWN: False, key.Z: False, key.X: False}
    key_action_time = { key.LEFT: 0, key.RIGHT: 0, key.UP: 0, key.DOWN: 0, key.Z: 0, key.X: 0}
    mouse_state = { 'is_down': False, 'x': 0, 'y': 0, 'time': 0}
    
    global game_window
    game_window = pyglet.window.Window(wwidth, wheight)
    #keyboard = key.KeyStateHandler()
    #game_window.push_handlers(keyboard)
    
    #global playerimage, playersprite
    #playerimage = pyglet.image.load("player.png")
    #playerimage.anchor_x = playerimage.width //2 
    #playerimage.anchor_y = playerimage.height //2 
    #playersprite = pyglet.sprite.Sprite(playerimage)
    
    global draw_function, loop_function
    
    global game_label, start_button_label, settings_label, quit_label, game_over_label
    game_label = pyglet.text.Label('shmupHell', 
                              font_name='Times New Roman', 
                              font_size=20,
                              x=game_window.width//2, y=game_window.height-24,
                              anchor_x='center', anchor_y='center')
    
    
    
    start_button_label = pyglet.text.Label('Start', 
                              font_name='Times New Roman', 
                              font_size=16,
                              x=game_window.width//2, y=game_window.height-200,
                              anchor_x='center', anchor_y='center')
    
    settings_label = pyglet.text.Label('Settings', 
                              font_name='Times New Roman', 
                              font_size=16,
                              x=game_window.width//2, y=game_window.height-300,
                              anchor_x='center', anchor_y='center')
    
    quit_label = pyglet.text.Label('Quit', 
                              font_name='Times New Roman', 
                              font_size=16,
                              x=game_window.width//2, y=game_window.height-400,
                              anchor_x='center', anchor_y='center')
    
    game_over_label = pyglet.text.Label('Game Over!', 
                              font_name='Times New Roman', 
                              font_size=16,
                              x=game_window.width//2, y=100,
                              anchor_x='center', anchor_y='center')
    
    global player, bullet_array, enemy_array 
    global draw_function, loop_function
    rebind_main_menu()
    
    global stage1
    stage1 = import_stage("stage1.csv")
    global current_stage
    
    global display_game_over
    display_game_over = False
    
    global fps_display 
    
    fps_display = pyglet.clock.ClockDisplay()
    pyglet.clock.set_fps_limit(30)

def draw_menu():   
    for i in range(0,3):
        glColor3f(1,1,1)
        glBegin(GL_POLYGON)
        glVertex2f(game_window.width//2-40, (game_window.height-200-100*i)-20)
        glVertex2f(game_window.width//2+40, (game_window.height-200-100*i)-20)
        glVertex2f(game_window.width//2+40, (game_window.height-200-100*i)+20)
        glVertex2f(game_window.width//2-40, (game_window.height-200-100*i)+20)
        glEnd()
        glColor3f(0,0,0)
        glBegin(GL_POLYGON)
        glVertex2f(game_window.width//2-38, (game_window.height-200-100*i)-18)
        glVertex2f(game_window.width//2+38, (game_window.height-200-100*i)-18)
        glVertex2f(game_window.width//2+38, (game_window.height-200-100*i)+18)
        glVertex2f(game_window.width//2-38, (game_window.height-200-100*i)+18)
        glEnd()
        glColor3f(1,1,1)
        
    game_label.draw()
    start_button_label.draw()
    settings_label.draw()
    quit_label.draw()
    
    if display_game_over:
        game_over_label.draw()
    

def draw_ingame():
    
    if player:
        if player.bomb_state:
            glColor3f(0.7,0.7,0.7) #gray when invulnerable
            glBegin(GL_POLYGON)
            for i in [2*math.pi*x/(player.bomb_radius/4+10) for x in range(0,int(player.bomb_radius/4+10))]:
                glVertex2f(player.bomb_x+player.bomb_radius*math.cos(i), player.bomb_y+player.bomb_radius*math.sin(i))
            glEnd()
            glColor3f(1,1,1)
        if player.invuln_time>0:
            glColor3f(0.5,0.5,0.5) #gray when invulnerable
        glBegin(GL_POLYGON) #player as diamond for now
        glVertex2f(player.x, player.y+4)
        glVertex2f(player.x-4, player.y)
        glVertex2f(player.x, player.y-4)
        glVertex2f(player.x+4, player.y)
        
        if player.invuln_time>0:
            glColor3f(1,1,1) #restore
        
        glEnd()

        
    ##global player
    ##playersprite.x=player.x
    ##playersprite.y=player.y
    ##playersprite.draw()
    
    if enemy_array:
        for enemy in enemy_array:
            glBegin(GL_POLYGON)
            glVertex2f(enemy.x-10, enemy.y-10)
            glVertex2f(enemy.x+10, enemy.y-10)
            glVertex2f(enemy.x+10, enemy.y+10)
            glVertex2f(enemy.x-10, enemy.y+10)
            glEnd()
    if bullet_array:
        for bullet in bullet_array:
            glBegin(GL_POLYGON)
            glVertex2f(bullet.x-2, bullet.y-2)
            glVertex2f(bullet.x+2, bullet.y-2)
            glVertex2f(bullet.x+2, bullet.y+2)
            glVertex2f(bullet.x-2, bullet.y+2)
            glEnd()    
    
def loop_menu(time):
    #print(display_mouse_state())
    #print(game_window.width//2-40, game_window.width//2+40, game_window.height-200-20, game_window.height-200+20)
    if mouse_state['is_down']==True and mouse_state['x'] >= game_window.width//2-40 and mouse_state['x'] <= game_window.width//2+40 and mouse_state['y'] >= game_window.height-200-20 and mouse_state['y'] <= game_window.height-200+20:
        rebind_ingame()
    if mouse_state['is_down']==True and mouse_state['x'] >= game_window.width//2-40 and mouse_state['x'] <= game_window.width//2+40 and mouse_state['y'] >= game_window.height-400-20 and mouse_state['y'] <= game_window.height-400+20:
        pyglet.app.exit()

    
def loop_ingame(time):
    if player.game_over:
        rebind_main_menu()
        global display_game_over
        display_game_over= True
        
    if key_state[key.LEFT]:
        player.moveleft(time)
    if key_state[key.RIGHT]:
        player.moveright(time)
    if key_state[key.UP]:
        player.moveup(time)
    if key_state[key.DOWN]:
        player.movedown(time)
    if key_state[key.Z]:
        player.fire()
    if key_state[key.X]:
        player.bomb()
    if player.bomb_state:
        if player.bomb_radius < 200:
            player.bomb_radius = player.bomb_radius + 1
        else:
            player.bomb_state = False
            player.bomb_radius = 0
    #print(player.invuln_time)
    if player.invuln_time > 0:
        player.invuln_time = player.invuln_time - 1
    #player.power = player.power + 0.01   

    current_stage.make_things_appear()

    global enemy_array, bullet_array

    if enemy_array:    
        enemy_array[:] = (enemy for enemy in enemy_array if not enemy.killyourself)
        for enemy in enemy_array:
            enemy.fire()
            enemy.move(time)
        

                
    if bullet_array:

        bullet_array[:] = (bullet for bullet in bullet_array if not bullet.killyourself)
        
        
        for bullet in bullet_array:
            bullet.hitcheck()
            bullet.move(time)

    #print(len(bullet_array))    
        
def create_entities():
    global bullet_array, enemy_array, player, cache_references, enemy_array
    bullet_array = []
    enemy_array = []


    player = Player(2, 3)
    global current_stage
    current_stage = copy.deepcopy(stage1)
    
    cache_references(player, bullet_array, enemy_array) 
    #boss = StageOneBoss()
    #boss.health = 5000
    #enemy_array.append(boss)

    current_stage.stage_activate(time.time())
    #enemy_array.append(Enemy(400,400,1, 0))
    #enemy_array.append(Enemy(200,400,1, 0))
    #enemy_array.append(Enemy(600,400,1, 0))
    #enemy_array[0].circ(450, 450)
    #enemy_array[1].circ(200, 250)
    #enemy_array[2].circ(650, 400)
                              
def rebind_main_menu():
    global draw_function, loop_function
    draw_function = draw_menu
    loop_function = loop_menu
    
def rebind_ingame():
    global draw_function, loop_function
    create_entities()
    draw_function = draw_ingame
    loop_function = loop_ingame
    
load_resources()


def display_key_state():
    return 'L:' + str(key_state[key.LEFT]) + ' UP:' + str(key_state[key.UP]) + ' DOWN:' + str(key_state[key.DOWN]) + ' R:' + str(key_state[key.RIGHT]) + ' Z:' + str(key_state[key.Z])

def display_mouse_state():
    return 'IsDown:' + str(mouse_state['is_down']) + ' x:' + str(mouse_state['x']) + ' y:' + str(mouse_state['y'])

@game_window.event
def on_key_press(symbol, modifiers):   
    key_state_modify(symbol, modifiers, True, time.time())
        
@game_window.event
def on_key_release(symbol, modifiers):
    key_state_modify(symbol, modifiers, False, time.time())
    
@game_window.event
def on_mouse_press(x, y, button, modifiers):
    mouse_state_modify(x, y, _button = button, _modifiers = modifiers, _is_down = True, _time = time.time())
        
@game_window.event
def on_mouse_release(x, y, button, modifiers):
    mouse_state_modify(x, y, _button = button, _modifiers = modifiers, _is_down = False, _time = time.time())

@game_window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_state_modify(x, y)

@game_window.event   
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    mouse_state_modify(x, y)

def mouse_state_modify(x, y, _button = None, _modifiers = None, _is_down = None, _time = None):
    mouse_state['x']=x
    mouse_state['y']=y
    
    if not _button ==None and _button == mouse.LEFT:
        if not _is_down == None:
            mouse_state['is_down']=_is_down       
        if not _time == None:
            mouse_state['time']=_time
        
def key_state_modify(symbol, modifiers, is_down, time):
    #if symbol >= key.LEFT and symbol <= key.DOWN or key.Z:
    key_state[symbol] = is_down
    key_action_time = time
        

def loop(time):
    loop_function(time)
    
   
@game_window.event
def on_draw():
    #game_window.clear()
    glClear(GL_COLOR_BUFFER_BIT) #clear buffer
    glLoadIdentity() #reset rotation matrix
    fps_display.draw()
    
    draw_function()
    
    glBegin(GL_LINE_LOOP) #mouse circle
    for theta in [x*2*math.pi/10 for x in range(0,10)]:
        glVertex2f(math.cos(theta)*5+mouse_state['x'], math.sin(theta)*5+mouse_state['y'])
    glEnd()

        
if __name__ == '__main__':
    pyglet.clock.schedule_interval(loop, 1/120)
    pyglet.app.run()    
