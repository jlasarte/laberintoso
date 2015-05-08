# -*- coding: utf-8 -*- #
"""
	PALABRAS: Clase para el manejo de las palabras del jeugo.
	
    LABERINTOSO: Juego didactico de laberinto

    Julia Lasarte <julia.lasarte@gmail.com>

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
    along with Laberitnoso.  If not, see <http://www.gnu.org/licenses/>.


"""
import shelve,os
from random import shuffle

class Palabras:
	
	def __init__(self):
		""" 
		Inicializa la clase, abre el archivo y controla excepcciones
		
		"""
		
		self.palabras = shelve.open(os.path.join('data','palabras', 'palabras.pal'))
		
	def addPalabra(self, palabra, imagen):
		"""
		Agrega una palabra el archivo
		
		@param palabra :  palabra a agregar
		@imagen: direccion de la imagen correspondiente a la palabra.
		
		"""
		p = {}
		p['palabra'] = palabra
		p['imagen'] = imagen
		p['letras'] = set()
		for c in palabra:
			p['letras'].add(c)
		
		self.palabras[palabra] = p
	
	def eliminarPalabra(self,palabra):
		"""
		Elimina una palabra del archivo
		devuelve si la v si se elimino, falso si no se pudo eliminar
		
		"""
		if self.palabras.has_key(palabra):
			del self.palabras[palabra]
			return True
		else:
			return False
	
	def getPalabras(self,letra,cant=0):
		"""
		Devuelve una lista de palabras que contienen una 
		determinada letra
		
		@param letra: letra a buscar
		@param cant: cantidad de letras a devolver.
		
		"""
		
		palabras = []
		for p in self.palabras.iterkeys():
			if letra in self.palabras[p]['letras']:
				palabras.append(self.palabras[p])
		
		if cant <> 0 and len(palabras)>cant:
			shuffle(palabras)
			palabras = palabras[0:cant]
		
		return palabras
		
	def getPalabrasSin(self,letra,cant=0):
		"""
		Devuelve una lista de palabras que no contienen una 
		determinada letra
		
		@param letra: letra a buscar
		@param cant: cantidad de letras a devolver.
		
		"""
		
		palabras = []
		for p in self.palabras.iterkeys():
			if not (letra in self.palabras[p]['letras']):
				palabras.append(self.palabras[p])
		
		if cant <> 0:
			shuffle(palabras)
			palabras = palabras[0:cant]
		
		return palabras
	
	def HasPalabras(self,letra):
		"""
	    The way you're blowing up my phone won't make leave no faster.
		
		@param letra: 
	
		"""
		tiene = False
		for p in self.palabras.iterkeys():
			if letra in self.palabras[p]['letras']:
				tiene = True
				break
		return tiene
		
	def Close(self):
		self.palabras.close()
		