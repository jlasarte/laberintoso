        # -*- coding: utf-8 -*- #

import pygame, sys,os
from pygame.locals import *
Regla = os.path.join('data','imagenes','help','REGLAS.jpg')
Coontrl = os.path.join('data','imagenes','help','CONTROL.jpg')
Enem = os.path.join('data','imagenes','help','ENEMIGO.jpg')
Pal1 = os.path.join('data','imagenes','help','PALABRAS1.jpg')
Pal2 = os.path.join('data','imagenes','help','PALABRAS2.jpg')
Pal3 = os.path.join('data','imagenes','help','PALABRAS3.jpg')
pygame.init()
Vent=pygame.display.set_mode((800,600))
pygame.display.set_caption('AYUDA')



def Pantalla(x):
  if x==1:
    fondo=pygame.image.load(Regla)
  elif x==2:
    fondo=pygame.image.load(Coontrl)
  elif x==3:
    fondo=pygame.image.load(Enem)
  elif x==4:
    fondo=pygame.image.load(Pal1)
  elif x==5:
    fondo=pygame.image.load(Pal2)
  elif x==6:
    fondo=pygame.image.load(Pal3)
  Vent.blit(fondo,(0,0))
  pygame.display.flip()


def MostrarAyuda():
  B=True
  x=1
  while(B):
    Pantalla(x)
    for event in pygame.event.get():
      if event.type == KEYDOWN and event.key == K_ESCAPE:
        B=False
      elif event.type == KEYDOWN and event.key == K_RIGHT:
        if x+1<7:
          x=x+1
        else:
          x=1
      elif event.type == KEYDOWN and event.key == K_LEFT:
        if x-1>0:
          x=x-1
        else:
          x=6
