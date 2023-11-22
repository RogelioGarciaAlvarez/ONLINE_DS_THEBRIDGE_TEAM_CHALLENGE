import clases
import funciones
import numpy as np
import random
import sys
import variables

#Instrucciones 
print("Bienvenidos al juego de hundir la flota 'El Victory'")
print("Las instrucciones son muy sencillas:")
print("-Hay dos jugadores: tú y la máquina. Empiezas tú")
print("-En cada tablero hay 4 barcos de 1 posición de eslora, 3 barcos de 2 posiciones de eslora, 2 barcos de 3 posiciones de eslora y 1 barco de 4 posiciones de eslora")
print("-El juego te pedirá al principio que selecciones un nivel de dificultad")
print("-Cuando sea tu turno tendrás que introducir las coordenadas de fila, primero, y columna, después, separadas por coma, cuyos valores deben estar entre 0 y 9")
print("-El orden de las filas y columnas es de arriba a abajo y de izquierda a derecha")
print("-Cada vez que aciertes te vuelve a tocar disparar. Si fallas, es el turno de la máquina que te disparará aleatoriamente")
print("-El juego finalizará cuando se hundan todos los barcos de algun jugador")
print("-Para salir del juego antes de que se hundan todos los barcos introduce la palabra 'exit' (sin comillas)\n")


#Se crean los tableros del usuario y de la máquina
tablero_usuario = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)
tablero_maquina = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)

#Se colocan los barcos indicados en el enunciado
for barco in variables.lista_barcos:

    tamano_barco = barco[1]

    for repeticion in range(barco[0]): 
        funciones.posicionar_aleatorio(tablero_usuario.tablero_barcos, tamano_barco, variables.DIMENSION_FILA-1, variables.DIMENSION_COLUMNA-1)
        funciones.posicionar_aleatorio(tablero_maquina.tablero_barcos, tamano_barco, variables.DIMENSION_FILA-1, variables.DIMENSION_COLUMNA-1)

#Preguntamos al usuario la dificultad en la que quiere jugar
dificultad = input("Indica la dificultad del juego entre estas opciones: facil, media y dificil:").lower()

#Seleccionamos la cantidad de disparos de la máquina en funcion de la dificultad
if dificultad == "facil" or dificultad == "media" or dificultad == "dificil":

    if dificultad =="facil": #si la dificultad es facil, la maquina tiene un disparo
        repeticion_maquina = 1
    elif dificultad =="media": #si la dificultad es media, la maquina tiene dos disparos
        repeticion_maquina = 2
    elif dificultad =="dificil": #si la dificultad es dificil, la maquina tiene tres disparos
        repeticion_maquina = 3

    #Iniciamos el juego con un while que finalizará si el usuario indica "exit" o no hay barcos en algun tablero
    fin_juego = False
    usuario = True

    while True:

        if usuario == True: #Si le toca al usuario

            tablero_a_disparar = tablero_maquina.tablero_barcos #Dispara el usuario
            tablero_registro_disparo = tablero_usuario.tablero_registro_disparos #Se guardan los disparos hechos por el usuario

            continuar = True
            while continuar == True: #Usamos el bucle while para disparar hasta que fallemos o hundamos todos los barcos
                
                #Pedimos al usuario que introduzca las coordenadas y las guardamos en una lista
                coordenadas_str = input("Tu turno. Introduce la coordenada de la fila y la coordenada de la columna separadas por coma:")
                coordenadas_lista = coordenadas_str.split(",")
                
                #Si el usuario introduce "exit", se acaba el juego
                if coordenadas_lista[0] == "exit":
                    print("Ha finalizado el juego")
                    sys.exit()

                continuar = funciones.disparo(tablero_a_disparar, tablero_registro_disparo, int(coordenadas_lista[0]), int(coordenadas_lista[1]), \
                                              variables.DIMENSION_FILA-1, variables.DIMENSION_COLUMNA-1) #Devuelve True si se debe seguir disparando y False en caso contrario

                #Se muestra el tablero de registro de disparos del usuario
                print("Tu tablero de registro de disparos:")
                print(tablero_usuario.tablero_registro_disparos)
                
                #Se comprueba si todos los barcos de la maquina han sido tocados
                fin_juego = funciones.comprobar_fin_juego(tablero_a_disparar)
                
                #En caso de que todos los barcos de la maquina esten tocados, el juego termina y el usuario gana
                if fin_juego == True: 
                    print("Has ganado")
                    sys.exit()
            
            usuario = False #Cambiamos para que sea el turno de la máquina

        elif usuario == False: #Si le toca a la máquina

            tablero_a_disparar = tablero_usuario.tablero_barcos #Dispara la maquina
            tablero_registro_disparo = tablero_maquina.tablero_registro_disparos #se guardan los disparos hechos por la maquina
            
            #Se usa un bucle for para que la máquina tenga tantos disparos como dificultad elegida
            for disparo_maquina in range(repeticion_maquina):

                continuar = True
                while continuar == True: #Usamos el bucle while para que la máquina dispare hasta que falle o hunda todos los barcos
                    
                    coordenada_fila_maquina = np.random.randint(0,variables.DIMENSION_FILA) #Genera coordenadas de disparo aleatorias
                    coordenada_columna_maquina = np.random.randint(0,variables.DIMENSION_COLUMNA) #Genera coordenadas de disparo aleatorias

                    continuar = funciones.disparo(tablero_a_disparar, tablero_registro_disparo, coordenada_fila_maquina, coordenada_columna_maquina, \
                                                  variables.DIMENSION_FILA-1, variables.DIMENSION_COLUMNA-1) #Devuelve True si se debe seguir disparando y False en caso contrario
                    
                    #Se comprueba si todos los barcos del usuario han sido tocados
                    fin_juego = funciones.comprobar_fin_juego(tablero_a_disparar)
                    
                    #En caso de que todos los barcos del usuario esten tocados, el juego termina y la maquina gana
                    if fin_juego == True: 
                        print("Ha ganado la máquina")
                        sys.exit()


            #Se muestra el tablero de barcos del usuario
            print("La máquina ha disparado. Asi ha quedado tu tablero de barcos:")
            print(tablero_usuario.tablero_barcos)
            
            usuario = True #Cambiamos para que sea el turno del usuario

#Si el usuario no ha introducido correctamente la dificultad, se pide volver a empezar
else:
    print("La dificultad elegida no es válida. Vuelve a empezar")