import numpy as np

#Se define la clase Tablero y como argumento al contructor se indica la dimension de las filas y de las columnas
class Tablero():
   
    def __init__(self, dimension_fila, dimension_columna):
        self.tablero_barcos = np.tile(" ", [dimension_fila, dimension_columna]) #Se crea un tablero de espacios vacios donde se colocaran los barcos
        self.tablero_registro_disparos = np.tile(" ", [dimension_fila, dimension_columna]) #Se crea un tablero de espacios vacios donde se registraran los disparos
        
        #El valor de la dimension de filas y columnas es de 10. Esto esta indicado en el archivo variables.py
        self.limite_filas = dimension_fila-1 #El limite de filas del tablero debe ser uno menos que la dimension de la fila (en este caso, 9) ya que empieza en 0
        self.limite_columnas = dimension_columna-1 #El limite de columnas del tablero debe ser uno menos que la dimension (en este caso, 9) ya que empieza en 0