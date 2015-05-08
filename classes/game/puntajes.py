# -*- coding: utf-8 -*- #
"""
	PUNTAJES: Modulo para guardar, ver y manejar los puntajes del juego.
	
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
import pickle;
from operator import itemgetter
# puntaje (nombre,puntaje,dia y hora, segundos)	
def ResetArchivo(archivo):
	f= open(archivo,'w')
	l = []
	pickle.dump(l, f)
	f.close()

def InsertInOrder(lista,elemento): #ingresa un nuevo puntaje, verificando si no esta el mismo nombre.
	if (len(lista)==0):
		lista.insert(0,elemento)
	else:
		nom=elemento[0]
		b=True
		for i in lista:
		   if(i[0] == nom):
			   b=False
			   if (i[1]<elemento[1]):
				   x=lista.index(i)
				   del lista[x]
				   lista.append(elemento)
				   break
		if(b):
			lista.append(elemento)

def GuardarPuntaje(puntaje,archivo):
	try : 
		f = open(archivo,'r')
	except (IOError):
		ResetArchivo(archivo)
		f= open(archivo,'r')
	finally:
		try:
			l = pickle.load(f)
		except (ValueError):
			ResetArchivo(archivo)
			f= open(archivo,'r')
			l = pickle.load(f)
		InsertInOrder(l,puntaje)
		f.close()
		f = open(archivo, "w")
		pickle.dump(l, f)
		f.close()
		
def MostrarPuntajes(archivo):
	f = open(archivo,"r")
	try:
		l = pickle.load(f)
	except (ValueError):
		ResetArchivo(archivo)
		f= open(archivo,'r')
		l = pickle.load(f)
	if l==[]:
		return l
	else:
		l= sorted(l, key = itemgetter(1), reverse=True)
		if len(l) >10:
			l = l[0:11]
		return l
	
