# -*- coding: utf-8 -*- #
"""
	SPRITES: Las sprites usadas en el juego: Boton, Balam, Jugador y Enemigo
	
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
	along with Laberintoso.	 If not, see <http://www.gnu.org/licenses/>.


"""
import pygame, os,time

class Boton(pygame.sprite.Sprite):
		"""
		
		Clase para los botones del juego.
		
		"""
	
		def __init__(self, ancho, altura,x,y, name,image):
				"""
				Inicializa la spire. 
				
				@param ancho: ancho del boton.
				@param altura: altura del boton.
				@param x: coordenada x inicial.
				@param y: coordenada y inicial.
				@param name: nombre del boton, se usa para determinar la acción de clickear el boton.
				@param image: imagen del boton.
				
				"""
			
				pygame.sprite.Sprite.__init__(self)
				self.alto = altura
				self.ancho = ancho
				self.x, self.y = x,y
				self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)
				self.name = name
				try:
					self.image = pygame.image.load(image).convert_alpha()
				except (pygame.error):
					self.image = pygame.Surface((altura,ancho))
					Font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
					self.image.blit(Font.render(name, 1, (0, 0, 255)),(x,y))
				#self.image = pygame.transform.scale(self.image, (altura, ancho))
							
		
		def draw(self,pantalla):
				"""
				Dibuja la sprite sobre la pantalla.
				
				"""
				#pygame.draw.rect(pantalla,self.color, (self.x,self.y,self.ancho,self.alto),4)
				pantalla.blit(self.image,(self.x,self.y))
		
		def setImage(self, image):
				"""
				Cambia la imagen del boton. 
				
				@param image: nueva imagen.
				
				"""
				self.image = pygame.image.load(image).convert_alpha()
				#self.image = pygame.transform.scale(self.image, (self.alto, self.ancho))
		

	
				
				
class Palabra(pygame.sprite.Sprite):
		"""
		
		Clase para las palabras del Juego.
		
		"""
		
		def __init__(self, ancho, altura,x,y,p):
				"""
				Inicializa la sprite. 
				
				@param ancho: ancho de la palabra.
				@param altura: altura de la palabra.
				@param x: coordenada x inicial.
				@param y: coordenada y inicial.
				@type p: dict
				@param p: palabra de la sprite. 
				
				
				"""			
				pygame.sprite.Sprite.__init__(self)
				self.alto = altura
				self.ancho = ancho
				self.x, self.y = x*self.ancho,y*self.alto
				self.coordx,self.coordy = x,y
				
				self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)
				
				try:
					self.image = pygame.image.load(os.path.join('data','palabras', p["imagen"]))
					self.image = pygame.transform.scale(self.image, (altura, ancho))
				except(pygame.error):
					self.image = pygame.Surface((altura,ancho))
					Font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
					self.image.blit(Font.render(p["palabra"], 1, (0, 0, 255)),(x,y))
				self.image.set_alpha(200)
				self.letras = p["letras"]
				self.palabra = p["palabra"]
				
		def contains(self,letra):
				return letra in self.letras

class Jugador(pygame.sprite.Sprite):
		"""
		
		Clase para el jugador del Juego.
		
		"""	

		def __init__(self, ancho, altura):		
				"""
				Inicializa la sprite. 
				
				@param ancho: ancho de la palabra.
				@param altura: altura de la palabra.				
				
				"""
				#: imagenes de la Sprite. Para animar.
				imagenesAnim = {
					'derecha': pygame.image.load(os.path.join('data','imagenes', 'derecha.png')).convert_alpha(),
					'izquierda': pygame.image.load(os.path.join('data','imagenes', 'corre.png')).convert_alpha(),
					'arriba': pygame.image.load(os.path.join('data','imagenes', 'arriba.png')).convert_alpha(),
					'abajo': pygame.image.load(os.path.join('data','imagenes', 'abajo.png')).convert_alpha(),
					'attack': False,
					'hit': False
				}
				self.images = {}
				self.alto = altura
				self.ancho = ancho
				self.color = (255,0,0)
				self.x = 0
				self.y = 0
				self.coordx,self.coordy = 0,0
				self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)
				self.images["derecha"] = self.SliceandDice(imagenesAnim["derecha"],4)
				self.images["izquierda"] = self.SliceandDice(imagenesAnim["izquierda"],4)
				self.images["arriba"] = self.SliceandDice(imagenesAnim["arriba"],4)
				self.images["abajo"] = self.SliceandDice(imagenesAnim["abajo"],4)
				self.image = self.images["derecha"][0]
				self.clear = pygame.image.load(os.path.join('data','imagenes', 'blankie.gif')).convert_alpha()
				#self.image = pygame.image.load(os.path.join('data','imagenes', 'bear.gif')).convert_alpha()
				self.image = pygame.transform.scale(self.image, (altura, ancho))

		def SliceandDice(self,master_image,cant):
				"""
				Recorta la imagen para poder animar.
				
				@type master_image: Surface.
				@param master_image: imagen a recortar.
				@param cant: cantidad de porciones a recortar.
				
				"""
				images = []
				master_width, master_height = master_image.get_size()
				w=master_width/cant
				h=master_height
				for i in xrange(int(master_width/w)):
						images.append(master_image.subsurface((i*w,0,w,h)))
				return images

		def draw(self,pantalla):
				#pygame.draw.rect(pantalla,self.color, (self.x,self.y,self.ancho,self.alto),4)
				pantalla.blit(self.image,(self.x,self.y))
		
		def setRect( self, x , y ):
			"""
			Set el rect de la sprite.
			
			"""
			self.x,self.y = self.coordx, self.coordy = x,y
			self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)
		
		def checkCollision(self,enemigos):
				return pygame.sprite.spritecollideany(self, enemigos) != None
								
				
		def update(self,direccion,pantalla,copyCat,enemigos):
				"""
				Actualiza la Sprite del jugador. Incluye animación. Pero que copado.
				
				@param direccion : dirección a moverse 'u', 'd', 'l', 'r'.
				@pantalla: Surface donde blitear el jugador.
				@copyCat: copy de pantalla para borrar la estela.
				
				"""
				delay = 60
				if direccion == 'u':
						for i in self.images["arriba"]:
							if self.checkCollision(enemigos):
								break
							pantalla.blit(copyCat,(0,0))
							self.y -= self.alto/4.0
							self.coordy -= 1/4.0
							self.image = pygame.transform.scale(i,(self.alto,self.ancho))
							self.draw(pantalla)
							pygame.time.delay(delay)
							pygame.display.flip()
				elif direccion == 'd':
					for i in self.images["abajo"]:
						if self.checkCollision(enemigos):
								break
						pantalla.blit(copyCat,(0,0))
						self.y += self.alto/4.0
						self.coordy += 1/4.0
						self.image = pygame.transform.scale(i,(self.alto,self.ancho))
						self.draw(pantalla)
						pygame.time.delay(delay)
						pygame.display.flip()
				elif direccion == 'r':
						for i in self.images["derecha"]:
							if self.checkCollision(enemigos):
								break
							pantalla.blit(copyCat,(0,0))
							self.x += self.ancho/4.0
							self.coordx += 1/4.0
							self.image = pygame.transform.scale(i,(self.alto,self.ancho))
							self.draw(pantalla)
							pygame.time.delay(delay)
							pygame.display.flip()
				elif direccion == 'l':
						for i in self.images["izquierda"]:
							if self.checkCollision(enemigos):
								break
							pantalla.blit(copyCat,(0,0))
							self.x -= self.ancho/4.0
							self.coordx -= 1/4.0
							self.image = pygame.transform.scale(i,(self.alto,self.ancho))
							self.draw(pantalla)
							pygame.time.delay(delay)
							pygame.display.flip()
							
				self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)
		


class Enemigo(pygame.sprite.Sprite):
		"""
		
		Clase para los enemigos del Juego.
		
		"""	
		def __init__(self, ancho, altura, x,y):
				"""
				Inicializa la sprite. 
				
				@param ancho: ancho del enemigo.
				@param altura: altura del enemigo.
				@param x: coordenada x inicial.
				@param y: coordenada y inicial.			
				
				"""
				pygame.sprite.Sprite.__init__(self) #: 
				self.alto = altura
				self.ancho = ancho
				self.color = (0,0,255)
				self.x, self.y = x*self.ancho,y*self.alto
				self.coordx,self.coordy = x,y
				self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)
				try:
					self.image = pygame.image.load(os.path.join('data','imagenes', 'enemy.png')).convert_alpha()
				except (pygame.error):
					self.image = pygame.Surface((altura,ancho))
					Font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
					self.image.blit(Font.render("ENEMIGO", 1, (0, 0, 255)),(x,y))
				self.image = pygame.transform.scale(self.image, (altura, ancho))
				self.camino = []

		def draw(self,pantalla):
				pantalla.blit(self.image,(self.x,self.y))
		
		def update(self,(x,y)):

			   self.x =x*self.ancho
			   self.y= y*self.alto
			   self.coordx= x
			   self.coordy = y
			   self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)

class Bala(Enemigo):
		"""
		
		Clase para las Balas del juego. Pum, pum
		
		"""
	
		def update(self,direccion,pantalla,copyCat):
				"""
				Actualiza la Sprite de la Bala. Incluye animación. Llame ya!
				
				@param direccion : dirección a moverse 'u', 'd', 'l', 'r'.
				@pantalla: Surface donde blitear el jugador.
				@copyCat: copy de pantalla para borrar la estela.
				
				"""
				delay = 60 #: entre frame y frame
				if direccion == 'u':
					for y in xrange(4):
						pantalla.blit(copyCat,(0,0))
						self.y -= self.alto/4
						self.coordy -= 1/4
						self.draw(pantalla)
						pygame.time.delay(delay)
						pygame.display.flip()
						
				elif direccion == 'd':
					for y in xrange(4):
						pantalla.blit(copyCat,(0,0))
						self.y += self.alto/4
						self.coordy += 1/4
						self.draw(pantalla)
						pygame.time.delay(delay)
						pygame.display.flip()
						
				elif direccion == 'r':
					for x in xrange(4):
						pantalla.blit(copyCat,(0,0))
						self.x += self.ancho/4
						self.coordx += 1/4
						self.draw(pantalla)
						pygame.time.delay(delay)
						pygame.display.flip()
						
				elif direccion == 'l':
					for x in xrange(4):
						pantalla.blit(copyCat,(0,0))
						self.x -= self.ancho/4
						self.coordx -= 1/4
						self.draw(pantalla)
						pygame.time.delay(delay)
						pygame.display.flip()
						
				self.rect = pygame.Rect(self.x,self.y,self.ancho,self.alto)