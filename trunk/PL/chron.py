#! /usr/bin/env python

import os, sys
import pygame
from adds import *

class chronometer(pygame.sprite.Sprite):

    def __init__(self, elapsed_time, pos_top, pos_left):

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(None, 32)

        self.ms_elapsed = 0
        self.seg_elapsed = 0
        self.min_elapsed = 0

        self.chron_clock = pygame.time.Clock()

        self.pos_top = pos_top
        self.pos_left = pos_left

        self.update_chronometer()

    def update_chronometer(self):

        self.ms_elapsed += self.chron_clock.tick()
        self.seg_elapsed += self.ms_elapsed/1000
        self.min_elapsed += self.seg_elapsed/60
        self.seg_elapsed = self.seg_elapsed % 60
        self.ms_elapsed = self.ms_elapsed % 1000

        return self.render_chronometer()


    def render_chronometer(self):
        self.image = self.font.render("TIME: {0:1.0f}:{1:02.0f}:{2:03.0f}".format(self.min_elapsed, self.seg_elapsed, self.ms_elapsed), 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = self.pos_top
        self.rect.top = self.pos_left
        self.rect.width += 10

        return self.rect