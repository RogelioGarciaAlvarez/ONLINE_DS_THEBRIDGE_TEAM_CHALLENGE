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

#El miercoles vemos como hacer para poner la cantidad y tamaño de los barcos que nos piden
#Tendriamos que meter en el archivo variables.py las cantidades y tamaños para traernoslo a main.py y hacer un for
