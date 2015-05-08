# -*- coding: utf-8 -*- #
"""
	CONSTANTES: Constantes usadas en el juego.
		
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
import os

SCREEN_SIZE = (800,600) #: Tamaño de la pantalla
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
FONT = os.path.join('data','font' , 'OratorStd.otf') #: Tipografía usada en el juego
BGROUND = os.path.join('data','imagenes', 'bground.jpg') #: Fondo para la pantalla principal
CONFBGROUND = os.path.join('data','imagenes', 'conf.jpeg') #: Fondo para la configuración
HIGHBGROUND = os.path.join('data','imagenes', 'cropHigh.jpg') #: Fondo para los mejores puntajes
MUSIC = os.path.join('data','sonido' , 'LoopConfiguracion.wav') #: Musica de fondo
PUNTAJES = os.path.join('data','puntajes.dat') #: Archivo donde se guardan los puntajes
GANO = os.path.join('data','imagenes','gano.jpg')
LEVEL = os.path.join('data','imagenes','level.jpeg')
TITLE = 'Laberintoso'

#: Datos del jugador
JUGADOR = {
	'nombre': 'anonimo',
	'puntos': 0,
	'vidas': 3,
	'tjuego': 0,
	
}

#: Configuración del juego
CONFIGURACION = {
	'TTS': True,
	'SCREEN_SIZE': (800,600),
	'MUSICA': True,
	'SONIDO': True,
	'NIVEL': 'Facil',
	'LETRA': 'a'
}

menu_options = [
	'jugar',
	'configurar',
	'Mostrar Ranking',
	'ayuda',
	'salir'
	]

menu_configuracion = [
	'Musica',
	'Sonido',
	'Dificultad',
	'Valores por defecto',
	'salir'
	]

yes_no = [
	'si',
	'no'
	]

dificultades=[
	'FACIL',
	'NORMAL',
	'DIFICIL'
	]

