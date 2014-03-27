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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('cannonball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.start = self.area.midbottom
        self.rect.midbottom = self.start
        self.flying = False
        self.trace = []
        self.var = 0

    def update(self):
        if self.flying:
            self.rect = self.calcnewpos(self.rect)

    def calcnewpos(self, rect):
        dx = 0
        dy = 0
        if len(self.trace) > 0:
            dx = self.trace[self.var][0] - self.rect.centerx
            dy = self.trace[self.var][1] - self.rect.centery
            self.var += 1
        return rect.move(dx, dy)

    def shoot(self, target):
        self.flying = True
        speed = 5
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        direction = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        diff = direction / speed
        inc = (dx / diff, dy / diff)
        currentpoint = (self.rect.centerx, self.rect.centery)
        while (0 <= currentpoint[0] <= 640) and (0 <= currentpoint[1] <= 480):
            currentpoint = (currentpoint[0] + inc[0], currentpoint[1] + inc[1])
            self.trace.append(currentpoint)
        ##print "dx, dy: ", dx, dy, "direction: ", direction, "diff: ", diff, inc, self.trace[0]

    def default(self):
        self.rect.midbottom = self.start
        self.flying = False
        self.var = 0
        self.trace = []

class Aim(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('aim.png')

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

class Ballon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.image, self.rect = load_png('ballon.png')
        self.speed = -2
        self.rect.topleft = (640, 10)
        self.area = screen.get_rect()
        self.inarea = False

    def update(self):
        if self.area.contains(self.rect):
            self.inarea = True
        else:
            if self.inarea:
                self.speed = -self.speed
        self.rect.move_ip(self.speed, 0)

    def default(self):
        self.rect.topleft = (640, 10)
        self.inarea = False
        self.speed = -2

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([110, 55])
        self.color = (0, 0, 0)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, 480)
        self.hit = 0
        self.miss = 0
        self.acc = 1
        self.change = False
        self.font = pygame.font.Font(None, 18)
        self.hit_text = self.font.render("Hit: {0}".format(self.hit), 1, (240, 240, 240))
        self.miss_text = self.font.render("Miss: {0}".format(self.miss), 1, (240, 240, 240))
        self.acc_text = self.font.render("Accuracy: {:.0%}".format(self.acc), 1, (240, 240, 240))
        self.alltext = (self.hit_text, self.miss_text, self.acc_text)
        y = 5
        for text in self.alltext:
                self.image.blit(text, (5, y))
                y += 15

    def update(self):
        y = 5
        if self.change:
            total = self.hit + self.miss
            if self.miss != 0:
                self.acc = float(self.hit) / total
            self.hit_text = self.font.render("Hit: {0}".format(self.hit), 1, (240, 240, 240))
            self.miss_text = self.font.render("Miss: {0}".format(self.miss), 1, (240, 240, 240))
            self.acc_text = self.font.render("Accuracy: {:.0%}".format(self.acc), 1, (240, 240, 240))
            self.alltext = (self.hit_text, self.miss_text, self.acc_text)
            self.image.fill(self.color)
            for text in self.alltext:
                self.image.blit(text, (5, y))
                y += 15
            self.change = False

    def inc_miss(self):
        self.miss += 1
        self.change = True

    def inc_hit(self):
        self.hit += 1
        self.change = True
