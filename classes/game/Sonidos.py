
#Cargamos sonidos,para usarlos en forma independiente. Cada sonido,
#pertenecera a la clase mixer.sound y tendra sus propias funciones.

import pygame, sys,os
from pygame.locals import *
from pygame import mixer

pygame.mixer.init()
Pum = os.path.join('data','sonido','pum.wav')
LConf = os.path.join('data','sonido','LoopConfiguracion.wav')
LJuego= os.path.join('data','sonido','LoopJuego.wav')
Opc= os.path.join('data','sonido','Opcion.wav')
Loser = os.path.join('data','sonido','Perdi.wav')
try:
	Lose = pygame.mixer.Sound(Loser)
	Opcion = pygame.mixer.Sound(Opc)
	LJue = pygame.mixer.Sound(LJuego)
	LCon= pygame.mixer.Sound(LConf)
	Agarro = pygame.mixer.Sound(Pum) 
except(pygame.error)