
# -*- coding: utf-8 -*- #
"""
    LABERINTOSO: Juego didactico de laberinto

    Julia Lasarte <julia.lasarte@gmail.com>, Mateo Fontanet <mate.edlp@gmail.com>

    This file is part of Laberintoso.

    Laberintoso is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Laberintoso is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Laberintoso.  If not, see <http://www.gnu.org/licenses/>.


"""
import pygame,os,time,random
from pygame.locals import *

from classes.game.juego import Juego
from classes.game.palabras import Palabras
from classes.game import ayuda
import classes.gui.inputbox as inputbox
import classes.gui.jmenu as jmenu
import classes.game.puntajes as puntajes

from constantes import *


def getNivel(config):
    
    NIVEL_FACIL = {'nivel': 0,'columnas': 4, 'filas': 4,'enemigos':0,'completo': False }
    NIVEL_NORMAL = {'nivel': 4,'columnas': 8, 'filas': 8,'enemigos':2,'completo': False }
    NIVEL_DIFICIL = {'nivel': 8,'columnas': 12, 'filas': 12,'enemigos':4,'completo': False }
    if config['NIVEL'] == 'Normal':
        return NIVEL_NORMAL
    elif config['NIVEL'] == 'Facil':
        return NIVEL_FACIL
    elif config['NIVEL'] == 'Dificil':
        return NIVEL_DIFICIL
        
def MostrarRanking(screen):
    try:
        fondo=pygame.image.load(HIGHBGROUND)
    except(pygame.error):
        fondo= pygame.Surface(SCREEN_SIZE)
    screen.blit(fondo,(0,0))
    pygame.display.set_caption('RANKING')
    p = puntajes.MostrarPuntajes(PUNTAJES)
    x,y,xpoint = 204,100,545
    i= 0
    if len(p)>0:
        Font = pygame.font.Font(FONT,25)
        for puntaje in p:
            y= y+40
            i +=1
            if i == 1:
                screen.blit(Font.render(str(i)+'.| '+puntaje[0], 1, RED), (x, y))
                screen.blit(Font.render(str(puntaje[1]),1,RED),(xpoint,y))
            else:
                screen.blit(Font.render(str(i)+'.| '+puntaje[0], 1, BLACK), (x, y))
                screen.blit(Font.render(str(puntaje[1]),1,BLACK),(xpoint,y))
    else:
        Font = pygame.font.Font(FONT,50)
        screen.blit(Font.render("NO HAY RANKING", 1, BLACK), (200, 250))
    pygame.display.flip()
    B=True
    while B:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                B=False



screen = pygame.display.set_mode(SCREEN_SIZE)
try:
    bground = pygame.image.load(BGROUND)  
except(pygame.error):
    bground = pygame.Surface(SCREEN_SIZE)

pygame.display.set_caption(TITLE)

try:
    pygame.mixer.music.load(MUSIC)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1,0)
except(pygame.error):
    CONFIGURACION["MUSICA"] = False


music = 1
#LOOPY LE LOUP
while pygame.event.poll().type != pygame.QUIT:
    
    if not CONFIGURACION['MUSICA'] and music:
        pygame.mixer.music.pause()
        music = 0
    elif CONFIGURACION['MUSICA'] and not music:
        pygame.mixer.music.unpause()
        music = 1
        
    screen.blit(bground,(0,0))
    selection = jmenu.run(menu_options,BLACK,30,font=FONT,light=10,justify=True,pos=('center','center'))
    if selection == 'jugar':
        SEGUIR = True
        JUGADOR['vidas'] = 3
        JUGADOR['puntos'] = 0
        nombre = inputbox.ask(screen, "NOMBRE")
        if nombre : JUGADOR['nombre'] = nombre
        letra = inputbox.ask(screen, "LETRA") 
        if letra and Palabras().HasPalabras(letra): 
            CONFIGURACION['LETRA'] =  letra
        elif letra:
            Font = pygame.font.Font(FONT,25)
            screen.blit(Font.render("No hay palabras con la letra "+letra, 1, BLACK), (190, 220))
            screen.blit(Font.render("por favor, elegi otra letra ", 1, BLACK), (200, 250))
            while not(letra and Palabras().HasPalabras(letra)): 
                letra = inputbox.ask(screen, "LETRA") 
            CONFIGURACION['LETRA'] =  letra
            
        NIVEL = getNivel(CONFIGURACION)
        
        pygame.init()
        while SEGUIR: 
                pygame.mixer.music.stop()
                NIVEL['nivel']+=1
                NIVEL['columnas']+=1
                NIVEL['filas']+=1
                if (NIVEL['nivel']%2):
                        NIVEL['enemigos']+=1
                NIVEL['completo'] = False
                g = Juego(CONFIGURACION,screen,NIVEL,JUGADOR)
                g.run()
                if g.nivel['completo']:
                                       vent=pygame.display.set_mode((800,600))
                                       pygame.display.set_caption('FIN')
                                       Imagenn=pygame.image.load(LEVEL)
                                       vent.blit(Imagenn,(0,0))
                                       Font = pygame.font.SysFont(pygame.font.get_default_font(), 100)
                                       screen.blit(Font.render(str(g.nivel['nivel']+1), 1, (0, 0, 255)), (390,240))
                                       pygame.display.flip()
                                       B=True
                                       while B:
                                            for event in pygame.event.get():
                                                    if event.type == KEYDOWN and event.key == K_RETURN:
                                                              B=False       
                puntaje = (JUGADOR['nombre'],JUGADOR['puntos'],time.strftime('%a, %d %b %Y' , time.localtime()),JUGADOR['tjuego'])
                puntajes.GuardarPuntaje(puntaje,PUNTAJES)
                SEGUIR = g.nivel['completo'] and (g.nivel["nivel"] < 15)
        if g.nivel["nivel"] == 15  and g.nivel['completo']:
            try:
                imagenGano = pygame.image.load(GANO)
            except(pygame.error):
                imagenGano = pygame.Surface(SCREEN_SIZE)
            screen.blit(imagenGano,(0,0))
            pygame.display.flip()
            B=True
            while B:
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        B=False   
        screen.blit(bground,(0,0))  
        
    elif selection == 'configurar':

        pygame.display.set_caption('Configuración')
        try:
            fondo=pygame.image.load(HIGHBGROUND)
        except(pygame.error):
            fondo= pygame.Surface(SCREEN_SIZE)
        pygame.display.flip()
        while True:
            screen.blit(fondo,(0,0))
            selection = jmenu.run(menu_configuracion,RED,30,font=FONT,light=10,justify=True,pos=('center','center'))
            if selection == 'Musica':
                selection = jmenu.run(yes_no,RED,30,font=FONT,light=10,justify=True,pos=('center','center'))
                if selection == 'si':
                     CONFIGURACION['MUSICA']=True                 
                if selection== 'no':
                     CONFIGURACION['MUSICA']=False
                                 
            elif selection == 'Sonido':
                selection = jmenu.run(yes_no,RED,30,font=FONT,light=10,justify=True,pos=('center','center'))
                if selection == 'si':
                    CONFIGURACION['SONIDO']=True
                if selection== 'no':
                    CONFIGURACION['SONIDO']=False

            elif selection == 'Dificultad':
                selection = jmenu.run(dificultades,RED,30,font=FONT,light=10,justify=True,pos=('center','center'))
                if selection == 'FACIL':
                    CONFIGURACION['NIVEL']='Facil'
                if selection== 'NORMAL':
                    CONFIGURACION['NIVEL']='Normal'
                if selection== 'DIFICIL':
                    CONFIGURACION['NIVEL']='Dificil'

            elif selection == 'Valores por defecto':
                CONFIGURACION['NIVEL']='Normal'
                CONFIGURACION['SONIDO']=True
                CONFIGURACION['MUSICA']=True
                
            elif selection == 'salir':
                break
    elif selection == 'Mostrar Ranking':
        
        MostrarRanking(screen)          
        
    elif selection == 'ayuda' :
        
        ayuda.MostrarAyuda()
        
    elif selection == 'salir' : 
        pygame.quit()
        break
