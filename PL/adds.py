#! /usr/bin/env python
import os, sys
import pygame
from pygame.locals import *

# Carrega imagens do jogo segundo um path definido
def load_image(name):
    # Une o nome da imagem ao path de imagens do jogo
    fullname = os.path.join("data", "images")
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Carregamento de imagem falhou:", fullname
        raise SystemExit, message
    image = image.convert() # Converte pixels da imagem
    return image