#!/usr/bin/env python
# coding: utf
'''Dumb jumping balls'''

import pygame
import random

SIZE = 640, 480

def intn(*arg):
    '''Return list of ints from arg tuple'''
    return map(int,arg)

def Init(sz):
    '''Turn PyGame on'''
    global screen, screenrect
    pygame.init()
    screen = pygame.display.set_mode(sz)
    screenrect = screen.get_rect()

class GameMode:
    '''Basic game mode'''
    def __init__(self):
        '''Set game mode up

        - Inittialize black background'''
        self.background = pygame.Color("black")

    def Events(self,event):
        '''Event parser'''
        pass

    def Draw(self, screen):
        '''Draw game field'''
        screen.fill(self.background)

    def Logic(self, screen):
        '''Game logic: what to calculate'''
        pass

    def Leave(self):
        '''What to do when leaving this mode'''
        pass

    def Init(self):
        '''What to do when entering this mode'''
        pass

class Ball:
    '''Simple ball class'''

    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        '''Create a ball from image'''
        self.fname = filename
        self.surface = pygame.image.load(filename)
        self.rect = self.surface.get_rect()
        self.speed = speed
        self.pos = pos
        self.newpos = pos
        self.active = True

    def draw(self, surface):
        '''Draw ball on the surface'''
        surface.blit(self.surface, self.rect)

    def action(self):
        '''Proceed some action'''
        if self.active:
            self.pos = self.pos[0]+self.speed[0], self.pos[1]+self.speed[1]

    def logic(self, surface):
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        x,y = self.pos
        dx, dy = self.speed
        if x < self.rect.width/2:
            x = self.rect.width/2
            dx = -dx
        elif x > surface.get_width() - self.rect.width/2:
            x = surface.get_width() - self.rect.width/2
            dx = -dx
        if y < self.rect.height/2:
            y = self.rect.height/2
            dy = -dy
        elif y > surface.get_height() - self.rect.height/2:
            y = surface.get_height() - self.rect.height/2
            dy = -dy
        self.pos = x,y
        self.speed = dx,dy
        self.rect.center = intn(*self.pos)

class Universe:
    '''Game universe'''

    def __init__(self, msec, tickevent = pygame.USEREVENT):
        '''Run an universe with msec tick'''
        self.msec = msec
        self.tickevent = tickevent

    def Start(self):
        '''Start running'''
        pygame.time.set_timer(self.tickevent, self.msec)

    def Finish(self):
        '''Shut down an universe'''
        pygame.time.set_timer(self.tickevent, 0)

class GameWithObjects(GameMode):
    '''Game mode with active objects'''

    def __init__(self, objects=[]):
        '''New game with active objects'''
        GameMode.__init__(self)
        self.objects = objects

    def locate(self, pos):
        '''Find objects under position pos'''
        return [obj for obj in self.objects if obj.rect.collidepoint(pos)]

    def Events(self, event):
        '''Event parser:

        - Prtform object action after every tick'''
        GameMode.Events(self, event)
        if event.type == Game.tickevent:
            for obj in self.objects:
                obj.action()

    def Logic(self, surface):
        '''Game logic

        - Calculate objects' impact
        '''
        GameMode.Logic(self, surface)
        for obj in self.objects:
            obj.logic(surface)

    def Draw(self, surface):
        '''Draw game field

        - Draw all the objects on the top of game field
        '''
        GameMode.Draw(self, surface)
        for obj in self.objects:
            obj.draw(surface)

class GameWithDnD(GameWithObjects):
    '''Game mode with drad-n-droppeble objects'''
    def __init__(self, *argp, **argn):
        '''- Initialize DnD'''
        GameWithObjects.__init__(self, *argp, **argn)
        self.oldpos = 0,0
        self.drag = None

    def Events(self, event):
        '''Event parser:

        - Support for draggin and dropping objects
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = self.locate(event.pos)
            if click:
                self.drag = click[0]
                self.drag.active = False
                self.oldpos = event.pos
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if self.drag:
                    self.drag.pos = event.pos
                    self.drag.speed = event.rel
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.drag:
                self.drag.active = True
                self.drag = None
        GameWithObjects.Events(self, event)

def __main__():
    '''Main game code'''
    global Game

    Init(SIZE)
    Game = Universe(50)

    Run = GameWithDnD()
    for i in xrange(5):
        x, y = random.randrange(screenrect.w), random.randrange(screenrect.h)
        dx, dy = 1+random.random()*5, 1+random.random()*5
        Run.objects.append(Ball("ball.gif",(x,y),(dx,dy)))

    Game.Start()
    Run.Init()
    again = True
    while again:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            again = False
        Run.Events(event)
        Run.Logic(screen)
        Run.Draw(screen)
        pygame.display.flip()
    Game.Finish()
    pygame.quit()

if __name__ == '__main__':
    __main__()
