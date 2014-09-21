#!/usr/bin/python

import pyglet
from pyglet.window import key
from pyglet.window import mouse
import math
from pyglet.gl import *

import time

from classes import *



#pyglet.resource.path = ['resources'] 
#pyglet.resource.reindex()
#image = pyglet.resource.image("file.png")

game_window = pyglet.window.Window(wwidth,wheight)
label = pyglet.text.Label('shmupHell', 
                          font_name='Times New Roman', 
                          font_size=20,
                          x=game_window.width//2, y=game_window.height-24,
                          anchor_x='center', anchor_y='center')


key_state = { key.LEFT: False, key.RIGHT: False, key.UP: False, key.DOWN: False}
key_action_time = { key.LEFT: 0, key.RIGHT: 0, key.UP: 0, key.DOWN: 0}
mouse_state = { 'is_down': False, 'x': 0, 'y': 0, 'time': 0}

@game_window.event
def on_key_press(symbol, modifiers):   
    key_state_modify(symbol, modifiers, True, time.time())
        
@game_window.event
def on_key_release(symbol, modifiers):
    key_state_modify(symbol, modifiers, False, time.time())
    
@game_window.event
def on_mouse_press(x, y, button, modifiers):
    mouse_state_modify(x, y, button, modifiers, True, time.time())
        
@game_window.event
def on_mouse_release(x, y, button, modifiers):
    mouse_state_modify(x, y, button, modifiers, False)

@game_window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_state_modify(x, y)

@game_window.event   
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    mouse_state_modify(x, y)

def mouse_state_modify(x, y, button = mouse.LEFT, modifiers = 0, is_down = mouse_state['is_down'], time = mouse_state['time']):
    if button == mouse.LEFT:
        mouse_state['is_down']=is_down
        mouse_state['x']=x
        mouse_state['y']=y
        mouse_state['time']=time
        
def key_state_modify(symbol, modifiers, is_down, time):
    if symbol >= key.LEFT and symbol <= key.DOWN:
        key_state[symbol] = is_down
        key_action_time = time

def create_entities():
    global player, bullet_array, enemy_array
    bullet_array = []
    enemy_array = []
    player = Player(10)
    cache_references(player, bullet_array, enemy_array)
    enemy_array.append(Enemy(500,500,100))
        
    
def loop(time):
    if key_state[key.LEFT]:
        player.moveleft()
    if key_state[key.RIGHT]:
        player.moveright()
    if key_state[key.UP]:
        player.moveup()
    if key_state[key.DOWN]:
        player.movedown()
    if enemy_array:
        for enemy in enemy_array:
            enemy.bullet_gen()
            enemy.move()
    if bullet_array:
        for bullet in bullet_array:
            if not bullet.killyourself:
                bullet.hitcheck()
                bullet.move()
            else:  
                bullet_array.remove(bullet)
    


@game_window.event
def on_draw():
    #game_window.clear()
    glClear(GL_COLOR_BUFFER_BIT) #clear buffer
    glLoadIdentity() #reset rotation matrix
    label.draw()

    glBegin(GL_LINE_LOOP) #mouse circle
    for theta in [x*2*math.pi/10 for x in range(0,10)]:
        glVertex2f(math.cos(theta)*5+mouse_state['x'], math.sin(theta)*5+mouse_state['y'])
    glEnd()
    
    if player:
        glBegin(GL_TRIANGLES) #player as triangle for now
        glVertex2f(player.x, player.y+40)
        glVertex2f(player.x-30, player.y)
        glVertex2f(player.x+30, player.y)
        glEnd()
    
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
            glVertex2f(enemy.x-2, enemy.y-2)
            glVertex2f(enemy.x+2, enemy.y-2)
            glVertex2f(enemy.x+2, enemy.y+2)
            glVertex2f(enemy.x-2, enemy.y+2)
            glEnd()
            
            
        
if __name__ == '__main__':
    create_entities()
    pyglet.clock.schedule_interval(loop, 1/60)
    pyglet.app.run()    
