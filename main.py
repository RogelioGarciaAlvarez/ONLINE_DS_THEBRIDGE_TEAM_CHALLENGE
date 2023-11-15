import clases
import funciones
import numpy as np
import random
import variables

#Se crean los tableros del usuario y de la máquina
tablero_usuario = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)
tablero_maquina = clases.Tablero(variables.DIMENSION_FILA, variables.DIMENSION_COLUMNA)

#Se colocan los barcos indicados en el enunciado
for barco in variables.lista_barcos:
    tamano_barco = barco[1]

    for repeticion in range(barco[0]): 
        funciones.posicionar_aleatorio(tablero_usuario.tablero_barcos, tamano_barco, (variables.DIMENSION_FILA-1), (variables.DIMENSION_COLUMNA-1))
        funciones.posicionar_aleatorio(tablero_maquina.tablero_barcos, tamano_barco, (variables.DIMENSION_FILA-1), (variables.DIMENSION_COLUMNA-1))

print("Tablero usuario")
print(tablero_usuario.tablero_barcos) 

print("Tablero maquina")
print(tablero_maquina.tablero_barcos)

#Iniciamos el juego con un while que finalizará si el usuario indica "exit" o no hay barcos en algun tablero
fin_juego = False
usuario = True

while fin_juego == False:
    #HAY QUE PROGRAMAR QUE SE SIGA DISPARANDO HASTA FALLAR
    if usuario == True: #Si le toca al usuario
        coordenadas_str = input("Tu turno. Introduce la coordenada de la fila y la coordenada de la columna separadas por coma:")
        coordenadas_lista = coordenadas_str.split(",")

        if coordenadas_lista[0] == "exit":
            print("Se ha finalizado el juego")
            break
            
        else:
            tablero_a_disparar = tablero_maquina.tablero_barcos #Dispara el usuario
            tablero_registro_disparo = tablero_usuario.tablero_registro_disparos #se guardan los disparos hechos por el usuario
        
            usuario = funciones.disparo(tablero_a_disparar, tablero_registro_disparo, int(coordenadas_lista[0]), int(coordenadas_lista[1])) 
            
            print("Tablero registro disparo usuario")
            print(tablero_usuario.tablero_registro_disparos)

            print("Tablero disparos recibidos usuario")
            print(tablero_usuario.tablero_barcos)
            print("Tablero registro disparo maquina")
            print(tablero_maquina.tablero_registro_disparos)

            print("Tablero disparos recibidos maquina")
            print(tablero_maquina.tablero_barcos)

    else: #Si le toca a la máquina
        tablero_a_disparar = tablero_usuario.tablero_barcos #Dispara la maquina
        tablero_registro_disparo = tablero_maquina.tablero_registro_disparos #se guardan los disparos hechos por la maquina
        
        coordenada_fila_maquina = np.random.randint(0,10)
        coordenada_columna_maquina = np.random.randint(0,10)

        usuario = funciones.disparo(tablero_a_disparar, tablero_registro_disparo, coordenada_fila_maquina, coordenada_columna_maquina)
        print("Tablero registro disparo usuario")
        print(tablero_usuario.tablero_registro_disparos)

        print("Tablero disparos recibidos usuario")
        print(tablero_usuario.tablero_barcos)

        print("Tablero registro disparo maquina")
        print(tablero_maquina.tablero_registro_disparos)

        print("Tablero disparos recibidos maquina")
        print(tablero_maquina.tablero_barcos)
    
    if fin_juego ==True:
        if usuario == True:
            print("Fin del juego. Ha ganado el usuario")
        if usuario == False:
            print("Fin del juego. Ha ganado la máquina")