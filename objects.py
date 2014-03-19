# -*- coding: utf-8 -*-

import os
import math
import pygame
from pygame.locals import *

def load_png(name):
    """ Load image and return image object """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image: ', fullname
        raise SystemExit, message
    return image, image.get_rect()

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, vector, target=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('cannonball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = self.area.center
        self.speed = 10
        self.vector = vector
        self.target = target

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):
            self.default()

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)

    def fly(self, target):
        self.target = target
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        z = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        if dy > 0:
            if dx > 0:
                angle = math.acos(dx / z)
            else:
                angle = math.acos(dy / z) + (0.5 * math.pi)
        elif dy < 0:
            if dx < 0:
                angle = math.acos(math.fabs(dx) / z) + math.pi
            else:
                angle = math.acos(math.fabs(dy) / z) + (1.5 * math.pi)
        z = 10
        self.vector = (angle, z)
        print "Mouse position: ", target, dx, dy, "Angle: ", angle * (180 / math.pi)

    def default(self):
        self.rect.center = self.area.center
        self.vector = (0, 0)

class Aim(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('aim.png')

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
