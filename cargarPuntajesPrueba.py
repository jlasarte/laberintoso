import classes.game.puntajes as puntajes
import os
PUNTAJES = os.path.join('data','puntajes.dat')

puntajes.ResetArchivo(PUNTAJES)
puntajes.GuardarPuntaje(('Guido Van Rossum',3200,'x',24),PUNTAJES)
puntajes.GuardarPuntaje(('Von Neumman',333,'x',12),PUNTAJES)
puntajes.GuardarPuntaje(('Pancho Dotto',1111,'x',1290),PUNTAJES)
puntajes.GuardarPuntaje(('Ricardo Fort',234,'x',66),PUNTAJES)
puntajes.GuardarPuntaje(('Julia',100,'x',44),PUNTAJES)
puntajes.GuardarPuntaje(('Juan',101,'x',32),PUNTAJES)
puntajes.GuardarPuntaje(('Mateo',4,'x',21),PUNTAJES)

