#Importamos las librerías
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.stats import chi2_contingency 
from scipy.stats import pearsonr

#Función describe_df (encargado: Marion)
def describe_df():

    """
    Función que calcula y muestra diferentes tipos de datos de un DataFrame

    Argumentos:
    Obtener tipos de columnas
    Calcular porcentaje de valores nulos
    Obtener valores únicos y porcentaje de cardinalidad

    Retorna:
    DataFrame: Devuelve un DataFrame que resume la información
    """
    #Cuerpo de la función
    
    return "X"



#Función tipifica_variables (encargado: Rogelio)
def tipifica_variables(df, umbral_categoria, umbral_continua):
    
    """
    Función que sugiere tipos para la tipificación de las variables (columnas) de un DataFrame.

    Argumentos:
    df (DataFrame): DataFrame cuyas variables queremos tipificar.
    umbral_categoria (int): valor límite para clasificar una variable como categórica.
    umbral_numerica (float): valor límite para clasificar una variable como numérica continua.

    Retorna:
    DataFrame: devuelve un DataFrame con cinco columnas: "nombre_variable", "tipo_variable", "cardinalidad", "cardinalidad_porcentaje" y "tipo_sugerido".
    """
    
    #Creamos una lista con el tipo de cada variable
    lista_tipos = []
    
    #EXTRA: creamos dos listas para guardar la cardinalidad de cada variable
    lista_cardinalidad = []
    lista_cardinalidad_porcentaje = []
    
    #Creamos una lista con la tipificación sugerida para cada variable
    lista_tipificacion = []

    #Sugerimos la tipificación de la variable y la guardamos en la lista
    for columna in df.columns:
        
        #Guardamos en la lista el tipo de cada variable
        lista_tipos.append(df[columna].dtypes)
        
        #Calculamos la cardinalidad y la guardamos en las listas
        cardinalidad = df[columna].nunique()
        lista_cardinalidad.append(cardinalidad)
    
        cardinalidad_porcentaje = round(cardinalidad/len(df)*100,2)
        lista_cardinalidad_porcentaje.append(cardinalidad_porcentaje)
        
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
    df_tipifica = pd.DataFrame({"nombre_variable": df.columns.tolist(), "tipo_variable":lista_tipos, "cardinalidad":lista_cardinalidad, "cardinalidad_porcentaje":lista_cardinalidad_porcentaje, "tipo_sugerido":lista_tipificacion})

    return df_tipifica 

#Función get_features_num_regression (encargado: Estela)
def get_features_num_regression(df: pd.DataFrame, target_col: str, umbral_corr: float, pvalue: float = None) -> list:
    #la funcion devuelve none si todas las comprobaciones dan error
    #primero: comprueba si la variable target esta en el dataframe
    if target_col not in df.columns: 
        print("Error:", target_col, "no es una columna del dataframe.")
        return None
    #segundo: comprueba si es una variable continua
    elif df[target_col].dtype != np.number:
        print("Error:", target_col, "no es una variable numérica continua.")
        return None
    #tercero: comprueba que el umbral de correlacion este entre 0 y 1
    elif not 0 <= umbral_corr <= 1:
        print("Error:", umbral_corr, "no es un número entre 0 y 1.")
        return None
    #cuarto: comprueba que el pvalue sea distinto de none
    elif pvalue is not None and (not isinstance(pvalue, float) or not 0 <= pvalue <= 1):
        print("Error:", pvalue, "no es un valor adecuado para el p-value.")
        return None

    #definimos la matriz de correlacion
    corr_matrix = df.corr()
    corr_target = corr_matrix[target_col]
    #devuelve las correlaciones que cumplen que el valor absoluto de cada correlacion es mayor que el valor del umbral de correlacion
    corr_target = corr_target[np.abs(corr_target) > umbral_corr]
    
    #si el pvalue no es none
    if pvalue is not None:
        #filtra las columnas numericas cuya correlacion con target_col es mayor en valor absoluto al umbral_corr
        #y que supera el test de hipotesis con pvalue mayor o igual a 1
        corr_target = corr_target[[i for i in corr_target.index if i != target_col and pvalue < 1 - stats.pearsonr(df[i], df[target_col])[1]]]
    #devuelve una lista con los índices de las columnas que cumplen las condiciones
    return corr_target.index.tolist()

#Función plot_features_num_regression (encargado: Rogelio)
def plot_features_num_regression(df, target_col, lista_columnas="", umbral_corr=0, umbral_pvalue=None, limite_pairplot=5):
    
    """
    Función que genera los gráficos pairplot de las variables (columnas) de un DataFrame dada una variable target numérica.

    Argumentos:
    df (DataFrame): DataFrame que contiene las variables para las que queremos generar los gráficos pairplot.
    target_col (string): Nombre de la variable del DataFrame considerada como target.
    lista_columnas (lista) = Nombres de las columnas del DataFrame para las que queremos generar los gráficos pairplot
    umbral_corr (float) = valor mínimo de correlación para seleccionar las variables.
    umbral_pvalue (float) = valor máximo de pvalue para seleccionar las variables.
    limite_pairplot (int) = valor máximo de variables a generar en los gráficos pairplot.

    Retorna:
    Lista: devuelve una lista con los nombres de las columnas numéricas que cumplen las condiciones.
    """
    
    #Comprobamos que los valores de entrada tienen el tipo correcto

    #Comprobamos para el argumento df
    error_df = False
    if not(isinstance(df, pd.DataFrame)):
        error_df = True

    #Comprobamos para el argumento target_col
    error_target_col = False
    if not(isinstance(target_col, str)):
        error_target_col = True

    if target_col not in df.columns.tolist():
        error_target_col = True
    
    elif df[target_col].dtypes != float:
        error_target_col = True

    #Comprobamos para el argumento lista_columnas
    error_lista_columnas = False
    if not(isinstance(lista_columnas, (list,str))):
        error_lista_columnas = True

    if lista_columnas == []:
        error_lista_columnas = True

    for columna in lista_columnas:
        
        if columna == target_col:
            error_lista_columnas = True

        if columna not in df.columns.tolist():
            error_lista_columnas = True

    #Comprobamos para el argumento umbral_corr
    error_umbral_corr = False
    if not(isinstance(umbral_corr, (int, float))):
        error_umbral_corr = True
        
    elif umbral_corr < 0 or umbral_corr > 1:
        error_umbral_corr = True

    #Comprobamos para el argumento umbral_pvalue
    error_umbral_pvalue = False
    if not(isinstance(umbral_pvalue, (int, float))):
        if umbral_pvalue != None:
            error_umbral_pvalue = True
    
    elif umbral_pvalue < 0 or umbral_pvalue > 1:
        error_umbral_pvalue = True

    #Comprobamos para el argumento limite_pairplot
    error_limite_pairplot = False
    if not(isinstance(limite_pairplot, int)):
        error_limite_pairplot = True

    elif limite_pairplot < 2:
        error_limite_pairplot = True

    #Comprobamos si ha habido algñun un error y mostramos el mensaje de error en cada caso
    error = error_df or error_target_col or error_lista_columnas or error_umbral_corr or error_umbral_pvalue or error_limite_pairplot
    if error: 
        if error_df:
            print("Introduce un DataFrame")
        elif error_target_col:
            print("Introduce un string con el nombre de la variable numérica target del DataFrame") 
        elif error_lista_columnas:
            print("Introduce una lista con los nombres de las columnas (sin incluir el target) del DataFrame a analizar")   
        elif error_umbral_corr:
            print("Introduce un valor entero o decimal para el umbral de correlación y que esté comprendido entre 0.0 y 1.0")   
        elif error_umbral_pvalue:
            print("Introduce un valor entero o decimal para el umbral del pvalue y que esté comprendido entre 0.0 y 1.0")
        elif error_limite_pairplot:
            print("Introduce un valor entero con el límite de variables a representar en el pairplot y que sea mayor o igual a 2")
    
        return None
        
    else:

        if lista_columnas == "":
            #Creamos una lista con las columnas numericas del DataFrame
            lista_columnas_numericas = []

            for columna in df:
                
                try: 
                    pd.to_numeric(df[columna], errors='raise')
                    lista_columnas_numericas.append(columna) 
                
                except:
                    pass
            
            #Creamos el DataFrame de correlaciones con el target y nos quedamos con las variables que superan el umbral  
            df_corr = df[lista_columnas_numericas].corr()[[target_col]].abs()
            lista_columnas_pairplot = df_corr[df_corr[target_col] > umbral_corr].index.tolist()

        else: 
            
            lista_columnas.append(target_col)
            df_corr = df[lista_columnas].corr()[[target_col]].abs()
            lista_columnas_pairplot = df_corr[df_corr[target_col] > umbral_corr].index.tolist()

        #Comprobamos si supera el test de correlación
        if umbral_pvalue != None:
            
            for columna in lista_columnas_pairplot.copy():
                #Calculamos el pvalue y comprobamos su valor
                pvalue = pearsonr(df[target_col], df[columna]).pvalue
                
                #print(f"El pvalue de {columna} es {pvalue}") # SOLO PARA PRUEBAS BORRAR ANTES DE ENTREGAR
                
                #Si el pvalue es mayor que el umbral se elimina la columna
                if pvalue > umbral_pvalue:
                    lista_columnas_pairplot.remove(columna)

        #Eliminamos el target de la lista de columnas para calcular cuántos gráficos hay que generar
        lista_columnas_pairplot.remove(target_col)
        num_graficos = (len(lista_columnas_pairplot) // (limite_pairplot-1))

        if len(lista_columnas_pairplot) % (limite_pairplot-1) != 0:
            num_graficos = num_graficos + 1

        #print(f"\nEl número de gráficos es: {num_graficos}\n")  # SOLO PARA PRUEBAS BORRAR ANTES DE ENTREGAR

        #Generamos los gráficos
        if num_graficos == 1:
            
            lista = lista_columnas_pairplot.copy()
            lista.append(target_col)
            
            sns.pairplot(df[lista], height=3, aspect=1.5)
            
        else:
            
            for i in range(0,num_graficos):
                #Creamos listas con las distintas columnas a relacionar con el target
                lista = lista_columnas_pairplot[(limite_pairplot-1)*i:(limite_pairplot-1)*i+(limite_pairplot-1)].copy()
                lista.append(target_col)
                
                #print(lista) # SOLO PARA PRUEBAS BORRAR ANTES DE ENTREGAR
                
                sns.pairplot(df[lista], height=2, aspect=1.5)

        return lista_columnas_pairplot


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
    """
    Descripción breve de lo que hace la función.

    Argumentos:
    param1 (tipo): Descripción de param1.
    param2 (tipo): Descripción de param2.

    Retorna:
    tipo: Descripción de lo que retorna la función.
    """
def plot_features_cat_regression(dataframe, target_col="", columns=[], pvalue=0.05, with_individual_plot=False):

    # Verificar los valores de entrada
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("El primer argumento debe ser un dataframe.")
    
    if target_col not in dataframe.columns:
        raise ValueError(f"La columna '{target_col}' no existe en el dataframe.")
    
    if not isinstance(columns, list):
        raise ValueError("El argumento 'columns' debe ser una lista.")
    
    if not all(col in dataframe.columns for col in columns):
        raise ValueError("Al menos una de las columnas especificadas en 'columns' no existe en el dataframe.")
    
    if not isinstance(pvalue, (float, int)):
        raise ValueError("El argumento 'pvalue' debe ser un número.")
    
    if not isinstance(with_individual_plot, bool):
        raise ValueError("El argumento 'with_individual_plot' debe ser un valor booleano.")
    
    # Si la lista 'columns' está vacía, asignar las variables numéricas del dataframe
    if not columns:
        columns = dataframe.select_dtypes(include=['number']).columns.tolist()
    
    # Almacenar las columnas que cumplen las condiciones
    significant_columns = []
    
    for col in columns:
        # Realizar el test de chi-cuadrado entre la variable categórica y la target
        contingency_table = pd.crosstab(dataframe[col], dataframe[target_col])
        _, p_val, _, _ = chi2_contingency(contingency_table)
        
        # Comprobar si el p-valor es significativo
        if p_val <= (1 - pvalue):
            significant_columns.append(col)
            
            # Si se especifica, plotear el histograma agrupado
    
            if with_individual_plot:
                sns.histplot(data=dataframe, x=target_col, hue=col, multiple="stack", kde=True)
                
    return significant_columns
