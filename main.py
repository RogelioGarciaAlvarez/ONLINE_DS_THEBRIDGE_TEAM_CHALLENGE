import pandas as pd
import numpy as np
import funciones
import clases
import variables

tablero_usuario = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)
tablero_maquina = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)


funciones.posicionar_aleatorio(tablero_usuario.tablero_barcos, 4)
funciones.posicionar_aleatorio(tablero_usuario.tablero_barcos, 4)
funciones.posicionar_aleatorio(tablero_usuario.tablero_barcos, 4)

print(tablero_usuario.tablero_barcos)  
print("Fin posicionamiento")

#HE VISTO QUE AUNQUE LO PONGO 3 VECES, A VECES PONE 3 BARCOS Y A VECES 2
#CREO QUE ESTO PASA PORQUE EN ALGUNA ORIENTACION NO ESTA MIRANDO BIEN SI SE SALE DE LOS LIMITES Y ESTA COLOCANDO UN BARCO FUERA.
#EL MIERCOLES LO REVISAMOS :)