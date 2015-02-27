#!/usr/bin/env python
# coding: utf

import pygame

SIZE = 640, 480

def Init(sz):
    '''Turn PyGame on'''
    global screen
    pygame.init()
    screen = pygame.display.set_mode(sz)

class GameMode:
    '''Basic game mode class'''

    def Events(self,event):
        '''Event parser'''
        pass

    def Draw(self, screen):
        pass

    def Logic(self):
        '''What to calculate'''
        pass

    def Leave(self):
        '''What to do when leaving this mode'''
        pass

    def Init(self):
        '''What to do when entering this mode'''
        pass

Init(SIZE)
Game = GameMode()

again = True
while again:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        again = False
    Game.Events(event)
    Game.Logic()
    Game.Draw(screen)
    pygame.display.flip()
pygame.quit()
