import numpy as np

def posicionar_aleatorio(tablero_barcos, tamano_barco, limite_filas =9 , limite_columnas = 9): #Ver como hacer el 9 de manera dinamica
    
    #Usamos un bucle while para generar la posicion y orientacion del barco aleatorio hasta que se pueda colocar en el tablero
    fuera_tablero = True
    while fuera_tablero == True:
        #Generamos dos números enteros aleatorios entre 0 y 9 que nos dará el origen para colocar el barco
        origen_fila = np.random.randint(10)
        origen_columna = np.random.randint(10)

        #Creamos una lista con la orientacion y la elegimos aleatoriamente
        orientacion = np.random.choice(["Norte", "Sur", "Este", "Oeste"])
        
        #Código para pruebas
        #print(f"Se ha generado un barco aleatoriamente de tamaño {tamano_barco} con orientacion {lista_orientacion[orientacion]}")
        #print(f"El barco tiene como origen la fila {origen_fila} y la columna {origen_columna}") 
        
        #Comprobamos si se puede posicionar el barco suponiendo que inicialmente no esta fuera del tablero (fuera_tablero == False)
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

            if orientacion == "Norte":
                #Se comprueba si ya hay un barco
                hay_barco = False #Inicializamos suponiendo que no hay barco
                barco_aleatorio = tablero_barcos[origen_fila-(tamano_barco-1):origen_fila+1, origen_columna:origen_columna+1]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X")) #Comprueba si hay algun True en la lista que genera .isin
                
                if hay_barco == False:   
                    tablero_barcos[origen_fila-(tamano_barco-1):origen_fila+1, origen_columna:origen_columna+1] = "O"

            elif orientacion == "Sur":
                #Se comprueba si ya hay un barco
                hay_barco = False #Inicializamos suponiendo que no hay barco
                barco_aleatorio = tablero_barcos[origen_fila:origen_fila+tamano_barco, origen_columna:origen_columna+1]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X"))

                if hay_barco == False:
                    tablero_barcos[origen_fila:origen_fila+tamano_barco, origen_columna:origen_columna+1] = "O"
            
            elif orientacion == "Este":
                #Se comprueba si ya hay un barco
                hay_barco = False #Inicializamos suponiendo que no hay barco
                barco_aleatorio = tablero_barcos[origen_fila:origen_fila+1, origen_columna:origen_columna+tamano_barco]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X"))

                if hay_barco == False:
                    tablero_barcos[origen_fila:origen_fila+1, origen_columna:origen_columna+tamano_barco] = "O"
    
            elif orientacion == "Oeste": #Oeste
                #Se comprueba si ya hay un barco
                hay_barco = False #Inicializamos suponiendo que no hay barco
                barco_aleatorio = tablero_barcos[origen_fila:origen_fila+1, origen_columna-(tamano_barco-1):origen_columna+1]
                hay_barco = np.any(np.isin(barco_aleatorio, "O")) or np.any(np.isin(barco_aleatorio, "X"))

                if hay_barco == False:
                    tablero_barcos[origen_fila:origen_fila+1, origen_columna-(tamano_barco-1):origen_columna+1] = "O"
        
        #else:
            #print("No se puede posicionar barco aleatorio\n") #Linea para comprobaciones
