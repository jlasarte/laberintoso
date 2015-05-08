# -*- coding: utf-8 -*- #
"""
    LABERINTO: Contiene la clase laberinto que genera el laberinto-matriz para el juego.
    
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
from random import choice


class Laberinto:
  
  def __init__(self, filas=30, columnas=40):
    """
    Inicializa la estructura para el laberinto con cantidad de Celdas x cantidad de Columnas.
    El laberinto es un diccionario donde para cada tupla de coordenadas, se guarda una celda.
    Para cada celda, se guarda la informacion 'abajo' y 'derecha' que representan una pared 
    (1: pared está, 0: pared derribada) y 'visitada' que se utiliza en el método generar() 
    para chequear si la celda fue o no visitada (DFS).

	@param filas : cantidad de filas del laberinto
	@param columnas: cantidad de columnas
	
    """

    self.filas = filas
    self.columnas = columnas
    self.laberinto = {}
    
    for y in xrange(filas):
      for x in xrange(columnas):
        # todas las paredes estan arriba, ninguna celda fue visitada
        celda = {'abajo' : 1, 'derecha' : 1, 'visitada': 0}
        self.laberinto[(x,y)] = celda
        
  def generate(self):
    """
    Genera el laberinto. El laberinto se trata como una matriz de adyacencia.
    usando una DFS iterativa se van "derribando paredes" en el laberinto.
    Idea para implementar un laberinto con DFS: http://www.mazeworks.com/mazegen/mazetut/index.htm
    Genera un laberinto "perfecto" : hay un y sólo un camino del comienzo al fin.

    """

    pila = []
    TotalCeldas= self.filas * self.columnas
    actual = self.laberinto[(self.columnas-1, self.filas-1)]
    Visitadas = 1
    
    # Mientras no hayamos visitado todas las celdas
    while (Visitadas < TotalCeldas):
      actual['visitada'] = 1
      vecinos =self.get_vecinos(actual)
      if len(vecinos)>0:
        # Elige un vecino al azar
        vecino = choice(vecinos)
        self.bajar_pared(actual,vecino)
        pila.append(actual)
        actual = vecino
        Visitadas += 1
      else:
        actual = pila.pop()

  def get_coords(self, cell):
    """
    Obtiene las coordenadas de una celda determinada
	
	@param celda: celda a buscar
	@return: coordenadas de la celda
	
    """

    coords = (-1, -1)

    for i in self.laberinto:
      if self.laberinto[i] is cell:
        coords = (i[0], i[1])
        break
        
    return coords

  def get_vecinos(self, cell):
    """
    Devuelve una lista de vecinos de la celda que se pasa como párametro
    sólo se agregan a la lista los vecinos que no han sido visitados
    """
        
    vecinos = []
    (x, y) = self.get_coords(cell)
    if (x, y) == (-1, -1):
      return vecinos
      
    # Calcula coordenadas de los vecinos	
    arriba = (x, y-1)
    abajo = (x, y+1)
    derecha = (x+1, y)
    izq = (x-1, y)
    
    if arriba in self.laberinto:
      if (self.laberinto[arriba]['visitada'] == 0):
        vecinos.append(self.laberinto[arriba])
    if abajo in self.laberinto:
      if (self.laberinto[abajo]['visitada']== 0):
        vecinos.append(self.laberinto[abajo])
    if derecha in self.laberinto:
      if (self.laberinto[derecha]['visitada']== 0):
        vecinos.append(self.laberinto[derecha])
    if izq in self.laberinto:
      if (self.laberinto[izq]['visitada']== 0):
        vecinos.append(self.laberinto[izq])

    return vecinos
    
  def bajar_pared(self, celda, vecino):
    """
    Baja la pared entre celda y vecino
	
    """
        
    xCelda, yCelda = self.get_coords(celda)
    xVecinio, yVecino = self.get_coords(vecino)

    # Que vecino?
    if xCelda == xVecinio and yCelda == yVecino + 1:
      # vecino arriba, derribar pared de abajo del vecino
      vecino['abajo'] = 0
    elif xCelda == xVecinio and yCelda == yVecino - 1:
      # vecino abajo, derribar pared de abajo de la celda
      celda['abajo'] = 0
    elif xCelda == xVecinio + 1 and yCelda == yVecino:
      # vecino a la izquierda, derribar pared de la derecha del vecino
      vecino['derecha'] = 0
    elif xCelda == xVecinio - 1 and yCelda == yVecino:
      # vecino a la derecha, derribar pared izquierda de la celda
      celda['derecha'] = 0
	  
	
  def get_ady(self, celda,laberinto):
    """
    Devuelve una lista de adyacentes de la celda que se pasa como párametro
    adyacentes son todas aquellas celdas "vecinas" a la celda parámetro
    que no tienen una pared dividiendolas. 

    """
  
    adyacentes = []
    (x, y) = self.get_coords(celda)
    if (x, y) == (-1, -1):
      return adyacentes
      
    # Calcula coordenadas de los adyacentes	
    arriba = (x, y-1)
    abajo = (x, y+1)
    derecha = (x+1, y)
    izq = (x-1, y)
    
    if arriba in self.laberinto:
      if (laberinto[arriba]['abajo'] == 0):
        adyacentes.append(self.laberinto[arriba])
    if abajo in self.laberinto:
      if (laberinto[(x,y)]['abajo']== 0):
        adyacentes.append(self.laberinto[abajo])
    if derecha in self.laberinto:
      if (laberinto[(x,y)]['derecha']== 0):
        adyacentes.append(self.laberinto[derecha])
    if izq in self.laberinto:
      if (laberinto[izq]['derecha']== 0):
        adyacentes.append(self.laberinto[izq])

    return adyacentes

  def resolver(self,celda = None,final= None ):
    """
    Resuelve el camino desde la celda hasta final. La resolucion es una versión 
    del algoritmo para "unweigthed shortest path" de grafos que se encuentra en : 
    WEISS, Mark Allen : "Data Structres and Algorithm Analysis in Java", Chapter 9: Graphs.
    Devuelve una lista de coordenadas, ordenadas de fin a principio.
	
	@param celda: comienzo del camino
	@param final: final del camino
	
    """
	
    cola = []   
	
	#copia del laberinto
    laberinto = self.laberinto
	
	# para cada celda, se agrega un campo distancia
    for y in xrange(self.filas):
      for x in xrange(self.columnas):
        laberinto[(x,y)]['dist'] = 0
		
    if celda is None:
      celda = (0, 0)

    laberinto[celda]['dist'] = 0
    cola.append(celda)

    while len(cola) > 0 :
       v = cola.pop()
       vecinos = self.get_ady(laberinto[v],laberinto)
       for vecino in vecinos:
         vCoords = self.get_coords(vecino)
         if laberinto[vCoords]['dist'] == 0:
           laberinto[vCoords]['dist'] = laberinto[v]['dist'] + 1
           cola.append(vCoords)
    
    # una vez que todas las celdas se marcaron, nos posicionamos en el último lugar
	# reccoriendo el laberinto "hacia atras" por las marcas de distancia hasta llegar al principio
    if final == None:
      actual = (self.filas-1,self.columnas-1)
    else:
      actual = final
    camino = []
    while not laberinto[actual]['dist'] == 1:
      vecinos = self.get_ady(laberinto[actual],laberinto)
      for vecino in vecinos:
        cords = self.get_coords(vecino)
        if laberinto[cords]['dist'] == laberinto[actual]['dist']-1:
          camino.append(cords)
	  actual = cords
	  break
	  
    return camino
		
   
