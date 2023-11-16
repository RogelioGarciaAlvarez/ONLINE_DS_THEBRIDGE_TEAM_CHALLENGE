import clases
import funciones
import numpy as np
import random
import sys
import variables

#Se crean los tableros del usuario y de la máquina
tablero_usuario = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)
tablero_maquina = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)

#Se colocan los barcos indicados en el enunciado
for barco in variables.lista_barcos:

    tamano_barco = barco[1]

    for repeticion in range(barco[0]): 
        funciones.posicionar_aleatorio(tablero_usuario.tablero_barcos, tamano_barco, variables.DIMENSION_FILA-1, variables.DIMENSION_COLUMNA-1)
        funciones.posicionar_aleatorio(tablero_maquina.tablero_barcos, tamano_barco, variables.DIMENSION_FILA-1, variables.DIMENSION_COLUMNA-1)

#Iniciamos el juego con un while que finalizará si el usuario indica "exit" o no hay barcos en algun tablero
fin_juego = False
usuario = True

while fin_juego == False:

    if usuario == True: #Si le toca al usuario
        
        tablero_a_disparar = tablero_maquina.tablero_barcos #Dispara el usuario
        tablero_registro_disparo = tablero_usuario.tablero_registro_disparos #se guardan los disparos hechos por el usuario

        continuar = True
        while continuar == True:
            
            coordenadas_str = input("Tu turno. Introduce la coordenada de la fila y la coordenada de la columna separadas por coma:")
            coordenadas_lista = coordenadas_str.split(",")

            if coordenadas_lista[0] == "exit":
                print("Ha finalizado el juego")
                sys.exit()

            continuar = funciones.disparo(tablero_a_disparar, tablero_registro_disparo, int(coordenadas_lista[0]), int(coordenadas_lista[1])) 

            print("Tablero registro disparo usuario")
            print(tablero_usuario.tablero_registro_disparos)

            print("Tablero disparos recibidos usuario")
            print(tablero_usuario.tablero_barcos)

            #print("Tablero registro disparo maquina")
            #print(tablero_maquina.tablero_registro_disparos)

            #print("Tablero disparos recibidos maquina")
            #print(tablero_maquina.tablero_barcos,"\n")
            
            fin_juego = funciones.comprobar_fin_juego(tablero_a_disparar)
        
            if fin_juego == True: 
                print("Ha ganado el usuario")
                sys.exit()
        
        usuario = False
               

    else: #Si le toca a la máquina
        tablero_a_disparar = tablero_usuario.tablero_barcos #Dispara la maquina
        tablero_registro_disparo = tablero_maquina.tablero_registro_disparos #se guardan los disparos hechos por la maquina

        continuar = True
        while continuar == True:
            
            coordenada_fila_maquina = np.random.randint(0,variables.DIMENSION_FILA)
            coordenada_columna_maquina = np.random.randint(0,variables.DIMENSION_COLUMNA)

            continuar = funciones.disparo(tablero_a_disparar, tablero_registro_disparo, coordenada_fila_maquina, coordenada_columna_maquina)
        
            #print("Tablero registro disparo usuario")
            #print(tablero_usuario.tablero_registro_disparos)

            #print("Tablero disparos recibidos usuario")
            #print(tablero_usuario.tablero_barcos)

            print("Tablero registro disparo maquina")
            print(tablero_maquina.tablero_registro_disparos)

            print("Tablero disparos recibidos maquina")
            print(tablero_maquina.tablero_barcos,"\n")
            
            fin_juego = funciones.comprobar_fin_juego(tablero_a_disparar)

            if fin_juego == True: 
                print("Ha ganado la máquina")
                sys.exit()

        usuario = True