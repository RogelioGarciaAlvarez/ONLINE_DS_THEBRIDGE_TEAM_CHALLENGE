import pandas as pd
import numpy as np
import funciones
import clases
import variables

tablero_usuario = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)
tablero_maquina = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)


funciones.posicionar_aleatorio(tablero_usuario.tablero_barcos, 4)

print(tablero_usuario.tablero_barcos)  
print("Fin posicionamiento")

#A VECES PONE 3 BARCOS, A VECES 2 Y A VECES 1
#EL MIERCOLES LO REVISAMOS :)