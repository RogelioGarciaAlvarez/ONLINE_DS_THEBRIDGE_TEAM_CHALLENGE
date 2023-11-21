import numpy as np

#Se define la clase Tablero en funcion de las variables dimension_fila y dimension_columna
class Tablero():
   
    def __init__(self, dimension_fila, dimension_columna):
        self.tablero_barcos = np.tile(" ", [dimension_fila, dimension_columna])
        self.tablero_registro_disparos = np.tile(" ", [dimension_fila, dimension_columna])
        #Las dimensiones de filas y columnas son 10
        self.limite_filas = dimension_fila-1 #El limite de filas del tablero debe ser uno menos que la dimension de la fila, en este caso, 9
        self.limite_columnas = dimension_columna-1 #El limite de columnas del tablero debe ser uno menos que la dimension de la columna, en este caso, 9