import numpy as np

class Tablero():
   
    def __init__(self, dimension_fila, dimension_columna):
        self.tablero_barcos = np.tile(" ", [dimension_fila, dimension_columna])
        self.tablero_disparos = np.tile(" ", [dimension_fila, dimension_columna])
        
        self.limite_filas = dimension_fila-1
        self.limite_columnas = dimension_columna-1