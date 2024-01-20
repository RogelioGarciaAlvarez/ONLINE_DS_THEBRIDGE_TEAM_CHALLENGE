#Importamos las librerías
import pandas as pd


#Función describe_df (encargado: Marion)
def describe_df():
    """
    Descripción breve de lo que hace la función.

    Argumentos:
    param1 (tipo): Descripción de param1.
    param2 (tipo): Descripción de param2.

    Retorna:
    tipo: Descripción de lo que retorna la función.
    """
    #Cuerpo de la función
    
    return "X"

#Función tipifica_variables (encargado: Rogelio)
def tipifica_variables(df, umbral_categoria, umbral_continua):
    
    """
    Función que sugiere tipos para la tipificación de las variables (columnas) de un DataFrame.

    Argumentos:
    df (DataFrame): DataFrame cuyas variables queremos tipificar
    umbral_categoria (int): valor límite para clasificar una variable como categórica
    umbral_numerica (float): valor límite para clasificar una variable como numérica continua

    Retorna:
    DataFrame: devuelve un DataFrame con tres columnas: "nombre_variable", "tipo_variable" y "tipo_sugerido".
    """
    #EXTRA: creamos una lista con el tipo de cada variable
    lista_tipos = []
    
    #Creamos una lista con la tipificación sugerida para cada variable
    lista_tipificacion = []

    #Sugerimos la tipificación de la variable y la guardamos en la lista
    for columna in df.columns:
        
        #EXTRA: Guardamos en la lista el tipo de cada variable
        lista_tipos.append(df[columna].dtypes)
        
        #Calculamos la cardinalidad
        cardinalidad = df[columna].nunique()
        
        #Clasificamos segun el valor de la cardinalidad
        if cardinalidad == 2:
            lista_tipificacion.append("Binaria")
            
        elif cardinalidad >= umbral_categoria:
            
            if cardinalidad >= umbral_continua:
                lista_tipificacion.append("Numérica continua")
                
            else: 
                lista_tipificacion.append("Numérica discreta")

        else:
            lista_tipificacion.append("Categórica")

    
    #Creamos el DataFrame con tantas filas como columnas tenga el DataFrame dado a la función
    df_tipifica = pd.DataFrame({"nombre_variable": df.columns.tolist(), "tipo_variable":lista_tipos, "tipo_sugerido":lista_tipificacion})

    return df_tipifica 

#Función get_features_num_regression (encargado: Marion)
def get_features_num_regression():
    """
    Descripción breve de lo que hace la función.

    Argumentos:
    param1 (tipo): Descripción de param1.
    param2 (tipo): Descripción de param2.

    Retorna:
    tipo: Descripción de lo que retorna la función.
    """
    #Cuerpo de la función
    
    return "X"

#Función plot_features_num_regression (encargado: Rogelio)
def plot_features_num_regression():
    """
    Descripción breve de lo que hace la función.

    Argumentos:
    param1 (tipo): Descripción de param1.
    param2 (tipo): Descripción de param2.

    Retorna:
    tipo: Descripción de lo que retorna la función.
    """
    #Cuerpo de la función
    
    return "X"


#Función get_features_cat_regression (encargado: Rogelio)
def get_features_cat_regression():
    """
    Descripción breve de lo que hace la función.

    Argumentos:
    param1 (tipo): Descripción de param1.
    param2 (tipo): Descripción de param2.

    Retorna:
    tipo: Descripción de lo que retorna la función.
    """
    #Cuerpo de la función
    
    return "X"

#Función plot_features_cat_regression (encargado: Numa)
def plot_features_cat_regression():
    """
    Descripción breve de lo que hace la función.

    Argumentos:
    param1 (tipo): Descripción de param1.
    param2 (tipo): Descripción de param2.

    Retorna:
    tipo: Descripción de lo que retorna la función.
    """
    #Cuerpo de la función
    
    return "X"