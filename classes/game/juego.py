# -*- coding: utf-8 -*- #
"""
        JUEGO: Clase principal, corre el juego
        
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
import pygame, sys,os, time, threading, math, puntajes
from pygame.locals import * 
from random import choice,randint

from laberinto import Laberinto
from palabras  import Palabras
from sprites   import Palabra,Enemigo,Jugador,Bala, Boton

#I mean, things can always go wrong.
try:
        import pyttsx
        engine = pyttsx.init() # talk to me, darling
        TTS = True
except ImportError:
        TTS = False

# Sonidos e imagenes del juego
BGROUND = os.path.join('data','imagenes', 'grass.jpg')
PERDI = os.path.join('data','imagenes','fin.jpg')
BOO = os.path.join('data','sonido','pum.wav')
SONIDO = os.path.join('data','imagenes', 'Sound.png')
MUTE = os.path.join('data','imagenes', 'Mute.png')
SALIR = os.path.join('data','imagenes','Power.png')
FONT = os.path.join('data','font' , 'OratorStd.otf')
PUNTAJES = os.path.join('data','puntajes.dat')
LJuego= os.path.join('data','sonido','LoopJuego.wav')
Perdi = os.path.join('data','sonido','Perdi.wav')

class Juego():
                """
                Clase del Juego.
                
                """
                
                def __init__(self,config,pantalla,nivel,jugador):                                  
                                """
                                Inicializa los datos de la partida. Se guardan los datos del jugador,
                                la letra con la cual se va a jugar, se carga la lista de palabras
                                y se inicializa el display. 
                                
                                @param nombre: nombre del jugador
                                @param config: datos de configuracion
                                @param pantalla: Surface sobre la cual se va a dibujar
                                @param nivel: datos del nivel. Cantidad de enemigos, letra, velocidad, etc.
                                
                                
                   
                                """
                                self.CONFIGURACION = config
                                try:
                                        pygame.mixer.music.load(LJuego)
                                except(pygame.error):
                                        self.CONFIGURACION['MUSICA'] = False 
                                try:
                                        self.Agarro = pygame.mixer.Sound(BOO)
                                except(pygame.error):
                                        self.CONFIGURACION['SONIDO'] = False 
                                self.botones = pygame.sprite.Group()
                                if self.CONFIGURACION['MUSICA']:
                                        self.music = 1
                                        pygame.mixer.music.play(-1,0)
                                        self.botones.add(Boton( 40, 40, 690, 550,'sound',SONIDO))
                                else:
                                        self.music = 0
                                        self.botones.add(Boton( 40, 40, 690, 550,'sound',MUTE))
                                        
                                self.botones.add(Boton( 40, 40, 630, 550,'salir',SALIR))
                                
                                
                                self.CONFIGURACION['TTS'] = TTS
                                self.datosJugador = jugador

                                #datos del nivel
                                self.nivel = nivel
                                
                                self.seguir = True
                                
                                #: letra con la cual se va a jugar
                                self.letra = self.CONFIGURACION['LETRA']
                                self.p = Palabras()
                                
                                # Cinco palabras con la letra a buscar, cino mal
                                self.listapalabras = self.p.getPalabras(self.CONFIGURACION['LETRA'],5*self.nivel['nivel'])
                                self.palabrasMal = self.p.getPalabrasSin(self.CONFIGURACION['LETRA'],5*self.nivel['nivel'])
                                
                                #inicializamos la pantalla
                                self.tam = (800,600)
                                self.pantalla = pantalla
                                #self.pantalla = pygame.display.set_mode(self.tam)
                                #pygame.display.set_caption('Laberinto')
                           
                                #ponemos un mensaje mientras se carga el laberinto y demás
                                font = pygame.font.SysFont(pygame.font.get_default_font(), 55)
                                text = font.render("Cargando...", 1, (255,255,255))
                                rect = text.get_rect()
                                rect.center = self.tam[0]/2, self.tam[1]/2
                                self.pantalla.blit(text, rect)
                                pygame.display.update(rect)
                                                 
                                                 
                def start_jugadores(self, cant=1):
                                """
                                Se inicializan las sprites del juego. Los enemigos se incializan
                                de acuerdo al número pasado como parámetro en cant y las palabras
                                según la cantidad que haya en la lista de palabras.
                                
                                @param cant: cantidad de enemigos
                                
                                """
                                #Sprite del jugador
                                self.jugador = Jugador(self.ancho_celda,self.alto_celda)
                                
                                #Grupos para enemigos y palabras
                                self.enemigos = pygame.sprite.Group()
                                self.palabras = pygame.sprite.Group()
                                self.pmal = pygame.sprite.Group()
                                
                                #inicializa enemigos y palabras en lugares random del laberinto
                                #Como el laberinto es perfecto - no hay ningún sector inaccesible, 
                                #no nos preocupamos por las coordenadas
                                for a in xrange(0,cant):
                                                self.enemigos.add(Enemigo(self.ancho_celda,self.alto_celda,randint(1,self.laberinto_obj.filas-1),randint(1,self.laberinto_obj.columnas-1)))
                                for p in self.listapalabras:
                                                pS = Palabra(self.ancho_celda,self.alto_celda,randint(1,self.laberinto_obj.filas-1),randint(1,self.laberinto_obj.columnas-1),p)
                                                while pygame.sprite.spritecollideany(pS, self.palabras) : pS = Palabra(self.ancho_celda,self.alto_celda,randint(1,self.laberinto_obj.filas-1),randint(1,self.laberinto_obj.columnas-1),p)
                                                self.palabras.add(pS)
                                for p in self.palabrasMal:
                                                pS = Palabra(self.ancho_celda,self.alto_celda,randint(1,self.laberinto_obj.filas-1),randint(1,self.laberinto_obj.columnas-1),p)
                                                while pygame.sprite.spritecollideany(pS, self.palabras) or pygame.sprite.spritecollideany(pS, self.pmal) : pS = Palabra(self.ancho_celda,self.alto_celda,randint(1,self.laberinto_obj.filas-1),randint(1,self.laberinto_obj.columnas-1),p)
                                                self.pmal.add(pS)
                
                def run(self):
                                """
                                Genera el laberinto, llama a los procesos que dibujan al
                                laberinto e inicializan sprites.
                                
                                """
                                self.stat = pygame.image.load(os.path.join('data','imagenes', 'stat.jpg')) 
                                self.laberinto_obj = Laberinto(self.nivel['filas'],self.nivel['columnas'])# args para cambiar tamano Laberinto(10,10) por ejemplo. Pa usar dps con la dificultad?
                                self.laberinto_obj.generate()
                                self.draw_laberinto()
                                self.start_jugadores(self.nivel['enemigos']) # pasa cantidad de enemigos
                                
                                for enemigo in self.enemigos.sprites():
                                                enemigo.camino = self.laberinto_obj.resolver((enemigo.coordx,enemigo.coordy),(randint(1,self.laberinto_obj.filas-1),randint(1,self.laberinto_obj.columnas-1))) 
                                self.reloj = pygame.time.Clock()
                                
                                self.loop()
                           

                def PuedeMov(self,direccion):
                                """
                                Chequea si el jugador puede moverse.
                                
                                @param direccion: direccion para la cual se chequea
                                @return: se puede mover?.
                                
                                """
                                (x,y) = (self.jugador.coordx,self.jugador.coordy)
                                arriba = (x, y-1)
                                izq = (x-1, y)
                                if direccion == 'up' :
                                                if not y == 0: #arriba del todo, no puede subir
                                                                if self.laberinto_obj.laberinto[arriba]['abajo'] == 0:
                                                                                return True
                                elif direccion == 'down': 
                                                if not y == self.laberinto_obj.filas -1: #abajo del todo
                                                                if self.laberinto_obj.laberinto[(x,y)]['abajo'] == 0:
                                                                                return True
                                elif direccion == 'right':
                                                if not x == self.laberinto_obj.columnas -1: #maximo derecha
                                                                if self.laberinto_obj.laberinto[(x,y)]['derecha']==0:
                                                                                return True
                                elif direccion == 'left':
                                                if not x == 0:
                                                                if self.laberinto_obj.laberinto[izq]['derecha'] == 0:
                                                                                return True
                                else:
                                                return False

                
                def draw_laberinto(self):
                                """
                                Dibuja el laberinto en pantalla.
                                
                                """
                                #a dibujar!
                                bground = pygame.image.load(BGROUND)
                                self.pantalla.blit(bground,(0,0))
                                self.ancho_celda = ((self.tam[0]-200)/self.laberinto_obj.columnas)# que tamaño tienen las celdas?
                                self.alto_celda = (self.tam[1]/self.laberinto_obj.filas)

                                for y in xrange(self.laberinto_obj.filas):
                                                for x in xrange(self.laberinto_obj.columnas):
                                                        if self.laberinto_obj.laberinto[(x, y)]['abajo']: # pared de abajo
                                                                pygame.draw.line(self.pantalla, (0,0,0), \
                                                                        (x*self.ancho_celda, y*self.alto_celda + self.alto_celda), \
                                                                        (x*self.ancho_celda + self.ancho_celda, \
                                                                        y*self.alto_celda + self.alto_celda) )
                                                        if self.laberinto_obj.laberinto[(x, y)]['derecha']: # pared de la derecha
                                                                pygame.draw.line(self.pantalla, (0,0,0), \
                                                                (x*self.ancho_celda + self.ancho_celda, y*self.alto_celda), \
                                                                (x*self.ancho_celda + self.ancho_celda, y*self.alto_celda + \
                                                                self.alto_celda) )
                                                                # Brde pantalla
                                pygame.draw.rect(self.pantalla, (0,0,0), (0,0, self.tam[0], self.tam[1]), 1)
                                pygame.display.update() # mostremos nuestros dibujillos
                                self.pantallaCopy = self.pantalla.copy()

                def solve(self):
                                """
                                Resuelve el laberinto desde la posición del jugador hasta la celda
                                final, ubicada en el extremo inferior derecho.
                                Para los primeros niveles.
                                
                                """
                                s = self.laberinto_obj.resolver((self.jugador.coordx,self.jugador.coordy))
                                for paso in s:
                                                pygame.draw.rect(self.pantalla, (0, 0, 0), (self.ancho_celda*paso[0]+5, self.alto_celda*paso[1]+5,\
                                                                                                                                          self.ancho_celda-10, self.alto_celda-10))
                                                pygame.display.update()
                                
                def MostrarEstado(self,Font,Biggie,p):
                                """
                                Muestra el estado del jugador. Vidas, puntos y tiempo de juego.
                                                                
                                """
                                # es tan lindo que me quiero morir. Morite, consola de comandos, morite.
                                self.pantalla.blit(self.stat,(601,1))
                                
                                if p: self.pantalla.blit(Biggie.render("PAUSED", 1, (0,0,0)), (240, 300))
                                
                                # datos player
                                self.pantalla.blit(Font.render(self.datosJugador["nombre"], 1, (86, 86, 86)), (705, 384))
                                self.pantalla.blit(Font.render("puntaje: "+str(self.datosJugador["puntos"]), 1, (86, 86, 86)), (705, 410))
                                self.pantalla.blit(Font.render("vidas: "+str(self.datosJugador["vidas"]), 1, (86, 86, 86)), (705, 430))
                                
                                
                                self.pantalla.blit(Biggie.render(self.letra,1,(255,255,255)),(625,380)) # letra con la que se está jugando
                                
                                #highscores
                                p = puntajes.MostrarPuntajes(PUNTAJES)
                                if len(p)>0:
                                        x,y = 630,460
                                        i = 0
                                        if len(p)>4: p = p[0:4]
                                        for puntaje in p:
                                                self.pantalla.blit(Font.render(puntaje[0][0:8] + ' - '+str(puntaje[1]) , 1, (10, 10, 0)), (x, y))
                                                if i==0: y +=23
                                                else: y+=17
                                                i+=1
                                
                def shoot(self, direccion):
                                """
                                Dispara una Bala.
                                
                                @direccion: up, down, left, right
                                
                                """
                                copyCat = self.pantalla.copy()
                                
                                self.bala = Bala(self.ancho_celda,self.alto_celda,0,0)
                                self.bala.image = pygame.image.load(os.path.join('data','imagenes', 'bala.png'))
                                self.bala.x= self.jugador.x
                                self.bala.y=self.jugador.y
                                while (pygame.sprite.spritecollideany(self.bala, self.pmal) == None)and(0<=self.bala.x < 600)and(0<=self.bala.y< 800):
                                        self.bala.update(direccion,self.pantalla,copyCat)
                                        self.bala.draw(self.pantalla)
                                if      pygame.sprite.spritecollideany(self.bala, self.pmal):
                                        self.pmal.remove(pygame.sprite.spritecollideany(self.bala,self.pmal))
                                        self.datosJugador['puntos'] += 10
                                
                def handleMouseDown(self,pos):
                                """
                                Maneja los clicks del mouse.
                                
                                @param pos: coordenadas del mouse.
                                
                                """                                             
                                
                                for boton in self.botones:
                                                
                                                if boton.rect.collidepoint(pos):
                                                        
                                                        if boton.name == 'salir':
                                                                
                                                                self.HiloEnemy.stop()
                                                                self.seguir = False
                                                                
                                                        elif boton.name == 'sound':
                                                                if self.music:
                                                                        pygame.mixer.music.pause()
                                                                        boton.setImage(MUTE)
                                                                        self.music = 0
                                                                elif not self.music and not self.CONFIGURACION['MUSICA']:
                                                                        pygame.mixer.music.play()
                                                                        boton.setImage(SONIDO)
                                                                        self.music = 1
                                                                else:
                                                                        pygame.mixer.music.unpause()
                                                                        boton.setImage(SONIDO)
                                                                        self.music = 1
                                
                                if self.CONFIGURACION['TTS']:
                                                for p in self.palabras:
                                                        if (p.rect.collidepoint(pos)):
                                                                engine.say(p.palabra)
                                                for p in self.pmal:
                                                        if (p.rect.collidepoint(pos)):
                                                                engine.say(p.palabra)
                                                        
                class EnemyThread(threading.Thread):
                                """
                                Hilo del enemigo. Para poder hacer hermoso delays. Probablemente hay una forma más facil? Perdón.
                                
                                """
                                def __init__(self,enemigos,lab,nivel):
                                                """
                                                It's the eye of the tiger.
                                                
                                                @param enemigos: sprites.
                                                @param lab: objeto laberinto, se usa para calcular el camino.
                                                @param nivel: nivel en el que se está jugando. Determina la velocidad del enemigo.
                                                
                                                """
                                                self.enemigos = enemigos
                                                self.laberinto_obj = lab
                                                self.seguir = True
                                                threading.Thread.__init__ ( self )
                                                self.pause = 0
                                                self.nivel = nivel

                                def run ( self ):
                                                """
                                                
                                                Corre el hilo del enemigo.
                                                
                                                """
                                                while self.seguir:
                                                        if math.log(self.nivel):
                                                                time.sleep(1.0/math.log(self.nivel))
                                                        else: time.sleep(1.5)
                                                        if not self.pause:                                              
                                                                for enemigo in self.enemigos.sprites():
                                                                                if len(enemigo.camino)>0:
                                                                                                enemigo.update(enemigo.camino.pop())
                                                                                else:
                                                                                                while len(enemigo.camino)==0:
                                                                                                                enemigo.camino = self.laberinto_obj.resolver((enemigo.coordx,enemigo.coordy),(randint(1,self.laberinto_obj.filas-1),randint(1,self.laberinto_obj.columnas-1)))
                                                                                                enemigo.update(enemigo.camino.pop())

                                                                
                                def stop(self):
                                                """
                                                Detiene el hilo.
                                                
                                                """
                                                self.seguir= False
                                

                                                
                def loop(self):
                                """
                                Loop principal del juego. Por ahora, lo unico que hace es seguir hasta que el juego se cierra
                                controlaría movienento del jugador, si agarro frutitas, blah blah.
                                
                                """
                                PAUSE = 0
                                vidas = 10
                                cache = 0
                                Font = pygame.font.Font(FONT,12)
                                Biggie =pygame.font.Font(FONT,60)
                                
                                self.HiloEnemy = self.EnemyThread(self.enemigos,self.laberinto_obj,self.nivel["nivel"])
                                self.HiloEnemy.start()
                                copyCat = self.pantalla.copy()

                                 # will block if lock is already hel
                                while self.seguir:
                                                
                                                if pygame.sprite.spritecollideany(self.jugador, self.enemigos) != None:
                                                        
                                                                #self.HiloEnemy.pause = True
                                                                self.jugador.setRect(0,0)
                                                                time.sleep(1)
                                                                self.datosJugador["vidas"] -=1
                                                                if self.CONFIGURACION['SONIDO'] :
                                                                        self.Agarro.play()                                                      
                                                                        
                                                for event in pygame.event.get():
                                                                if event.type == QUIT :
                                                                                self.HiloEnemy.stop()
                                                                                pygame.quit()
                                                                                sys.exit()
                                                                else:
                                                                                
                                                                                if event.type == KEYDOWN:
                                                                                                if not PAUSE:
                                                                                                                if event.key == K_UP: #arriba
                                                                                                                                if self.PuedeMov('up'):
                                                                                                                                                self.jugador.update('u',self.pantalla,copyCat,self.enemigos)
                                                                                                                if event.key == K_DOWN: #abajo
                                                                                                                                if self.PuedeMov('down'):
                                                                                                                                                self.jugador.update('d',self.pantalla,copyCat,self.enemigos)
                                                                                                                if event.key == K_RIGHT: #derecha
                                                                                                                                if self.PuedeMov('right'):
                                                                                                                                                self.jugador.update('r',self.pantalla,copyCat,self.enemigos)            
                                                                                                                if event.key == K_LEFT: #izuierda
                                                                                                                                if self.PuedeMov('left'):
                                                                                                                                                self.jugador.update('l',self.pantalla,copyCat,self.enemigos)
                                                                                                                if event.key == K_s:
                                                                                                                                self.solve()
                                                                                                                                time.sleep(1)
                                                                                                                if event.key == K_a:
                                                                                                                                self.shoot('l')
                                                                                                                if event.key == K_w:
                                                                                                                                self.shoot('u')
                                                                                                                if event.key == K_d:
                                                                                                                                self.shoot('r')
                                                                                                                if event.key == K_x:
                                                                                                                                self.shoot('d')
                                                                                                if event.key == K_p:
                                                                                                                PAUSE = 1 - PAUSE
                                                                                                                self.HiloEnemy.pause = 1 - self.HiloEnemy.pause
                                                                                if event.type == MOUSEBUTTONDOWN:
                                                                                                self.handleMouseDown(pygame.mouse.get_pos())
                                                                                                
                                                if pygame.sprite.spritecollideany(self.jugador,self.palabras) != None:
                                                                self.datosJugador["puntos"] += 50
                                                                self.palabras.remove(pygame.sprite.spritecollideany(self.jugador,self.palabras))
                                                if pygame.sprite.spritecollideany(self.jugador,self.pmal) != None:
                                                                if self.CONFIGURACION['SONIDO'] :
                                                                        self.Agarro.play()
                                                                self.datosJugador["puntos"] -= 50
                                                                self.pmal.remove(pygame.sprite.spritecollideany(self.jugador,self.pmal)) 
                                                if not len(self.palabras.sprites()):
                                                        self.HiloEnemy.stop()
                                                        self.nivel['completo']= True
                                                        self.seguir= False
                                                self.pantalla.blit(self.pantallaCopy,(0,0))
                                                self.palabras.draw(self.pantalla)
                                                self.MostrarEstado(Font,Biggie,PAUSE)
                                                self.enemigos.draw(self.pantalla)
                                                self.botones.draw(self.pantalla)
                                                
                                                #ygame.draw.rect(self.pantalla,(86, 86, 86),self.salir)
                                                self.pmal.draw(self.pantalla)
                                                
                                                copyCat = self.pantalla.copy()
                                                self.jugador.draw(self.pantalla)
                                        
                                                pygame.display.flip()
                                                if self.CONFIGURACION['TTS']: engine.runAndWait()
                                                if self.datosJugador["vidas"] == 0:
                                                        pygame.mixer.music.stop()
                                                        try:
                                                            perdi = pygame.mixer.Sound(Perdi)
                                                        except(pygame.error):
                                                            self.CONFIGURACION['MUSICA'] = False 
                                                        perdi.play()
                                                        self.HiloEnemy.stop()
                                                        self.nivel['completo']= False
                                                        self.seguir= False
                                                        try:
                                                                fondo = pygame.image.load(PERDI)
                                                        except(pygame.error):
                                                                fondo = pygame.Surface((800,600))
                                                        self.pantalla.blit(fondo,(0,0))
                                                        pygame.display.flip()
                                                        B=True
                                                        while B:
                                                                for event in pygame.event.get():
                                                                        if event.type == KEYDOWN and event.key == K_RETURN:
                                                                                B=False       
