import numpy as np

def posicionar_aleatorio(tablero_barcos, tamano_barco, limite_filas , limite_columnas): 
    #Usamos un bucle while para generar la posicion y orientacion del barco aleatorio hasta que se pueda colocar en el tablero
    barco_colocado = False
    while barco_colocado == False:
        #Generamos dos números enteros aleatorios entre 0 y 9 que nos dará el origen para colocar el barco
        origen_fila = np.random.randint(limite_filas)
        origen_columna = np.random.randint(limite_columnas)

        #Creamos una lista con la orientacion y la elegimos aleatoriamente
        orientacion = np.random.choice(["Norte", "Sur", "Este", "Oeste"])
     
        #Comprobamos si se puede posicionar el barco suponiendo que inicialmente no esta fuera del tablero
        fuera_tablero = False
        if orientacion == "Norte":
            if origen_fila - (tamano_barco-1) < 0:
                fuera_tablero = True
        
        elif orientacion == "Sur":
            if (limite_filas - origen_fila) < (tamano_barco-1):
                fuera_tablero = True
        
        elif orientacion == "Este":
            if (limite_columnas - origen_columna) < (tamano_barco-1):
                fuera_tablero = True
        
        elif orientacion == "Oeste":
            if origen_columna - (tamano_barco-1) < 0:
                fuera_tablero = True

        #Si no hay coordenadas fuera del tablero, se posiciona el barco siempre y cuando no haya otro barco
        if fuera_tablero == False:
            hay_barco = False #Inicializamos suponiendo que no hay barco
            if orientacion == "Norte":
                #Se comprueba si ya hay un barco
                barco_aleatorio = tablero_barcos[origen_fila-(tamano_barco-1):origen_fila+1, origen_columna:origen_columna+1]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X")) #Comprueba si hay algun True en la lista que genera .isin
                
                if hay_barco == False:   
                    tablero_barcos[origen_fila-(tamano_barco-1):origen_fila+1, origen_columna:origen_columna+1] = "O"
                    barco_colocado = True

            elif orientacion == "Sur":
                #Se comprueba si ya hay un barco
                barco_aleatorio = tablero_barcos[origen_fila:origen_fila+tamano_barco, origen_columna:origen_columna+1]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X"))

                if hay_barco == False:
                    tablero_barcos[origen_fila:origen_fila+tamano_barco, origen_columna:origen_columna+1] = "O"
                    barco_colocado = True
            
            elif orientacion == "Este":
                #Se comprueba si ya hay un barco
                barco_aleatorio = tablero_barcos[origen_fila:origen_fila+1, origen_columna:origen_columna+tamano_barco]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X"))

                if hay_barco == False:
                    tablero_barcos[origen_fila:origen_fila+1, origen_columna:origen_columna+tamano_barco] = "O"
                    barco_colocado = True
    
            elif orientacion == "Oeste":
                #Se comprueba si ya hay un barco
                barco_aleatorio = tablero_barcos[origen_fila:origen_fila+1, origen_columna-(tamano_barco-1):origen_columna+1]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X"))

                if hay_barco == False:
                    tablero_barcos[origen_fila:origen_fila+1, origen_columna-(tamano_barco-1):origen_columna+1] = "O"
                    barco_colocado = True


def disparo(tablero_a_disparar, tablero_registro_disparo, coordenada_fila, coordenada_columna, limite_filas = 9 , limite_columnas = 9):
    #Comprobamos si todas las coordenadas dadas para el disparo se pueden ubicar en el tablero
    if coordenada_fila > limite_filas or coordenada_columna > limite_columnas:
        print(f"Coordenadas incorrectas") 
        print(f"Recuerda que para las filas debes introducir un número entero comprendido entre el 0 y el 9")
        print(f"Recuerda que para las columnas debes introducir un número entero comprendido entre el 0 y el 9\n")

    #Se comprueba el elemento que contiene la casilla para sustituir el espacio vacio por el caracter adecuado
    else:
        tocado = False
        casilla = tablero_a_disparar[coordenada_fila:coordenada_fila+1, coordenada_columna:coordenada_columna+1]

        if casilla == "O": 
            tablero_a_disparar[coordenada_fila:coordenada_fila+1, coordenada_columna:coordenada_columna+1] = "X"
            tablero_registro_disparo[coordenada_fila:coordenada_fila+1, coordenada_columna:coordenada_columna+1] = "X"
            tocado = True
            return tocado
        
        elif casilla == "X":
            print("Ya habia un disparo en esas coordenadas")
            tocado = True
            return tocado
        
        else:
            tablero_a_disparar[coordenada_fila:coordenada_fila+1, coordenada_columna:coordenada_columna+1] = "-"
            tablero_registro_disparo[coordenada_fila:coordenada_fila+1, coordenada_columna:coordenada_columna+1] = "-"
            tocado = False
            return tocado


def comprobar_fin_juego(tablero_barcos): 
    fin = not(np.any(np.isin(tablero_barcos, "O")))
    return fin 

