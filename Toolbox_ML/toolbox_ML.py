#Importamos las librerías
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from scipy.stats import chi2_contingency #Test Chi2
from scipy.stats import f_oneway #Analisis de varianza o Anova
from scipy.stats import mannwhitneyu #Prueba U de Man-Whitney
from scipy.stats import pearsonr
from sklearn.feature_selection import mutual_info_classif
import warnings 
warnings.filterwarnings("ignore")

from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error



#Función describe_df (encargado: Marion)
def describe_df(df):
    """
    Función que calcula y muestra diferentes tipos de datos de un DataFrame

    Argumentos:
    df (DataFrame): DataFrame cuyas variables queremos describir.

    Retorna:
    DataFrame: Devuelve un DataFrame que resume la información
    """
    
    # Obtener tipos de columnas
    tipos = df.dtypes

    # Calcular porcentaje de valores nulos
    porcentaje_faltante = (df.isnull().mean() * 100).round(2)

    # Obtener valores únicos y porcentaje de cardinalidad
    valores_unicos = df.nunique()
    porcentaje_cardinalidad = ((valores_unicos / len(df)) * 100).round(2)

    # Crear un DataFrame con la información recopilada
    resultado_df = pd.DataFrame({
        'Tipos': tipos,
        '% Faltante': porcentaje_faltante,
        'Valores Únicos': valores_unicos,
        '% Cardinalidad': porcentaje_cardinalidad
    })

    return resultado_df.T

#############################################################################################################################

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

#############################################################################################################################

#Función get_features_num_regression (encargado: Estela)
def get_features_num_regression(df: pd.DataFrame, target_col: str, umbral_corr: float, pvalue: float = None) -> list:
    
    """
    Función que devuelve una lista con las variables numéricas de un dataframe cuya correlación con la variable target sea superior en valor absoluto al valor del umbral de correlación.
    Si el pvalue es distinto de None, sólo devolvera las variables numéricas cuya correlación supere el valor indicado y además supere el test de hipótesis con significación mayor o igual a 1-pvalue.
    
    Argumentos:
    df (DataFrame): DataFrame que queremos evaluar.
    target_col (string): Nombre de la variable del DataFrame considerada como target.
    umbral_corr (float): umbral de correlación que debe estar entre 0 y 1.
    pvalue (float) = valor por defecto None.

    Retorna:
    Lista: devuelve una lista con los nombres de las columnas que cumplen las condiciones.
    """
    
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
    corr_matrix = df.corr(numeric_only=True)
    corr_target = corr_matrix[[target_col]].abs()
    
    #devuelve las correlaciones que cumplen que el valor absoluto de cada correlacion es mayor que el valor del umbral de correlacion
    corr_target = corr_target[corr_target[target_col] > umbral_corr]
    
    #si el pvalue no es none
    if pvalue is not None:
        #filtra las columnas numericas cuya correlacion con target_col es mayor en valor absoluto al umbral_corr
        #y que supera el test de hipotesis con pvalue mayor o igual a 1
        corr_target = corr_target.loc[[i for i in corr_target.index if i != target_col and pvalue > pearsonr(df[i], df[target_col])[1]]]
    
    lista_variables = corr_target.index.tolist()
    
    if pvalue is None:
        # quitamos el target del DataFrame
        lista_variables.remove(target_col)
        
    #devuelve una lista con los índices de las columnas que cumplen las condiciones
    return lista_variables

#############################################################################################################################

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

    #Comprobamos si ha habido algun un error y mostramos el mensaje de error en cada caso
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
                
                #Si el pvalue es mayor que el umbral se elimina la columna
                if pvalue > umbral_pvalue:
                    lista_columnas_pairplot.remove(columna)

        #Eliminamos el target de la lista de columnas para calcular cuántos gráficos hay que generar
        lista_columnas_pairplot.remove(target_col)
        num_graficos = (len(lista_columnas_pairplot) // (limite_pairplot-1))

        if len(lista_columnas_pairplot) % (limite_pairplot-1) != 0:
            num_graficos = num_graficos + 1

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
                
                sns.pairplot(df[lista], height=2, aspect=1.5)

        return lista_columnas_pairplot

#############################################################################################################################

#Función get_features_cat_regression (encargado: Rogelio)
def get_features_cat_regression(df, target_col, umbral_pvalue=0.05):
    
    """
    Función que devuelve una lista con las variables (columnas) categóricas de un DataFrame que superan el test de relación con confianza estadística dada otra variable target numérica.
  
    Argumentos:
    df (DataFrame): DataFrame que contiene las variables para las que queremos evaluar la relación con confianza estadística.
    target_col (string): Nombre de la variable del DataFrame considerada como target.
    umbral_pvalue (float) = valor máximo de pvalue para seleccionar las variables.

    Retorna:
    Lista: devuelve una lista con los nombres de las columnas que cumplen las condiciones.
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

    #Comprobamos para el argumento umbral_pvalue
    error_umbral_pvalue = False
    if not(isinstance(umbral_pvalue, (int, float))):
        error_umbral_pvalue = True
    
    elif umbral_pvalue < 0 or umbral_pvalue > 1:
        error_umbral_pvalue = True

    #Comprobamos si ha habido algun un error y mostramos el mensaje de error en cada caso
    error = error_df or error_target_col or error_umbral_pvalue
    if error: 
        if error_df:
            print("Introduce un DataFrame")
        elif error_target_col:
            print("Introduce un string con el nombre de la variable numérica target del DataFrame")  
        elif error_umbral_pvalue:
            print("Introduce un valor entero o decimal para el umbral del pvalue y que esté comprendido entre 0.0 y 1.0")
    
        return None
        
    else:
        
        #Creamos una lista con las columnas numericas del DataFrame
        lista_columnas_categoricas = df.select_dtypes(include=['object']).columns.tolist()

        #Comprobamos si superan el test de correlación
        for columna in lista_columnas_categoricas.copy():
            
            if df[columna].nunique() == 2: #Variable categórica binaria --> U Mann-Withney

                #Creamos una lista con los dos valores de la variable
                valores = df[columna].unique().tolist()
                
                #Calculamos el pvalue y comprobamos su valor
                grupo_a = df.loc[df[columna] == valores[0], target_col]
                grupo_b = df.loc[df[columna] == valores[1], target_col]
                pvalue = mannwhitneyu(grupo_a, grupo_b).pvalue
            
            else: #Variable categórica no binaria --> ANOVA

                #Obtenemos los valores únicos de la variable categórica
                valores = df[columna].unique()

                #Creamos una lista donde guardar los distintos grupos
                lista_grupos = []
                
                #Separamos los datos en tantos grupos como valores tenga la variable categorica
                for valor in valores:
                    lista_grupos.append(df.loc[df[columna] == valor, target_col])

                #Calculamos el pvalue y comprobamos su valor
                pvalue = f_oneway(*lista_grupos).pvalue #El operador * lo que hace es separar todos los elementos de la lista y pasarselos como argumento a la función
                
            #Si el pvalue es mayor que el umbral se elimina la columna
            if pvalue > umbral_pvalue:
                lista_columnas_categoricas.remove(columna)

        return lista_columnas_categoricas

#############################################################################################################################

#Función plot_features_cat_regression (encargado: Numa)

"""
    Realiza un análisis de las características categóricas en relación con una variable objetivo en un dataframe, 
    identificando las características significativas y, opcionalmente, trazando histogramas agrupados.

    Argumentos:
    dataframe (pd.DataFrame): El dataframe que contiene los datos.
    target_col (str): El nombre de la columna que representa la variable objetivo.
    columns (list): Una lista de nombres de columnas categóricas para analizar. Si no se proporciona, 
                    se utilizarán todas las columnas numéricas del dataframe.
    pvalue (float): El nivel de significancia para considerar una característica como significativa en el análisis.
    with_individual_plot (bool): Indica si se deben trazar histogramas agrupados para las características significativas.

    Retorna:
    list: Una lista de nombres de columnas categóricas que se consideran significativas en relación con la variable objetivo.
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
        columns = dataframe.select_dtypes(include=['object']).columns.tolist()
    
    # Almacenar las columnas que cumplen las condiciones
    significant_columns = []
    
    for col in columns:
        # Realizar el test de chi-cuadrado entre la variable categórica y la target
        contingency_table = pd.crosstab(dataframe[col], dataframe[target_col])
        _, p_val, _, _ = chi2_contingency(contingency_table)
        
        # Comprobar si el p-valor es significativo
        if p_val <= pvalue:
            significant_columns.append(col)
            
    # Si se especifica, plotear el histograma agrupado
    num_graficos = len(significant_columns) // 2
    
    if len(significant_columns) % 2 != 0:
        num_graficos = num_graficos + 1
    
    if with_individual_plot:
        fig, axs = plt.subplots(num_graficos, 2, figsize=(20, 20))
        axs= axs.flatten()
      
    # Recorrer la lista de nombres de columnas y crear textos en cada subgráfico
        for i in range(len(significant_columns)):
            sns.histplot(data= dataframe,x = target_col , hue = significant_columns[i], ax= axs[i], kde=True)

        if len(significant_columns) % 2 != 0: 
            axs[-1].axis("Off")
                
    return significant_columns

#############################################################################################################################
  
#Función eval_model (encargado: Marion)
  
def eval_model(target, predicciones, tipo_de_problema, metricas):
    """
    Evalúa un modelo de Machine Learning utilizando diferentes métricas 

    Argumentos:
    target (tipo array): Valores reales del target
    predicciones (tipo array): Valores predichos por el modelo
    tipo_de_problema (str): puede ser de 'regresion' o 'clasificacion'
    metricas (list): Lista de métricas a calcular y a mostrar:
                     Para problemas de regresión: 'RMSE', 'MAE', 'MAPE', 'GRAPH'
                     Para problemas de clasificación: 'ACCURACY', 'PRECISION', 'RECALL', 'CLASS_REPORT', 'MATRIX', 'MATRIX_RECALL', 'MATRIX_PRED', 'PRECISION_X', 'RECALL_X'

    Retorna:
    tupla: Una tupla con los valores de las métricas especificadas en el orden indicado de la lista de métricas
    """

    results = []

    #REGRESION

    if tipo_de_problema == 'regresion':
        for metrica in metricas:
            
            if metrica == 'RMSE':
                rmse = np.sqrt(mean_squared_error(target, predicciones))
                print(f"RMSE: {rmse}")
                results.append(rmse)
            
            elif metrica == 'MAE':
                mae = mean_absolute_error(target, predicciones)
                print(f"MAE: {mae}")
                results.append(mae)

            elif metrica == 'MAPE':
                try:
                    mape = np.mean(np.abs((target - predicciones) / target)) * 100
                    print(f"MAPE: {mape}")
                    results.append(mape)

                #Imprimir ValueError
                except ZeroDivisionError:
                    raise ValueError("No se puede calcular MAPE cuando hay valores de target iguales a cero.")
           
            elif metrica == 'GRAPH':
                plt.figure(figsize=(8, 6))
                plt.scatter(target, predicciones)
                plt.xlabel('Real')
                plt.ylabel('Predicción')
                plt.title('Gráfico de dispersión de Predicciones vs Real')
                plt.show()

     #CLASIFICACION
                
    elif tipo_de_problema == 'clasificacion':
        for metrica in metricas:
            
            if metrica == 'ACCURACY':
                accuracy = accuracy_score(target, predicciones)
                print(f"Accuracy: {accuracy}")
                results.append(accuracy)

            elif metrica == 'PRECISION':
                precision = precision_score(target, predicciones, average='macro')
                print(f"Precision: {precision}")
                results.append(precision)

            elif metrica == 'RECALL':
                recall = recall_score(target, predicciones, average='macro')
                print(f"Recall: {recall}")
                results.append(recall)

            elif metrica == 'CLASS_REPORT':
                print("Classification Report:")
                print(classification_report(target, predicciones))

            elif metrica == 'MATRIX':
                print("Confusion Matrix (Absolute Values):")
                print(confusion_matrix(target, predicciones))

            elif metrica == 'MATRIX_RECALL':
                disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(target, predicciones))
                disp.plot(normalize='true')
                plt.title('Confusion Matrix (Normalized by Recall)')
                plt.show()

            elif metrica == 'MATRIX_PRED':
                disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(target, predicciones))
                disp.plot(normalize='pred')
                plt.title('Confusion Matrix (Normalized by Prediction)')
                plt.show()

            elif 'PRECISION_' in metrica:
                class_label = metrica.split('_')[-1] # Obtener la etiqueta de clase de la métrica
                try:
                    precision_class = precision_score(target, predicciones, labels=[class_label])
                    print(f"Precision for class {class_label}: {precision_class}")
                    results.append(precision_class)
                except ValueError:
                    raise ValueError(f"La clase {class_label} no está presente en las predicciones.")
                
            elif 'RECALL_' in metrica:
                class_label = metrica.split('_')[-1]
                try:
                    recall_class = recall_score(target, predicciones, labels=[class_label])
                    print(f"Recall for class {class_label}: {recall_class}")
                    results.append(recall_class)
                except ValueError:
                    raise ValueError(f"La clase {class_label} no está presente en las predicciones.")
    else:
        raise ValueError("El tipo de problema debe ser 'regresion' o 'clasificacion'.")

    return tuple(results)

#############################################################################################################################

#Función get_features_num_classification (encargado: Rogelio)

def get_features_num_classification(df, target_col, umbral_discreta=10, umbral_pvalue=0.05):
    """
    Función que devuelve una lista con las variables (columnas) numéricas de un DataFrame que superan el test de relación con confianza estadística dada otra variable target categórica.
  
    Argumentos:
    df (DataFrame): DataFrame que contiene las variables para las que queremos evaluar la relación con confianza estadística.
    target_col (string): Nombre de la variable del DataFrame considerada como target.
    umbral_discreta (int): valor máximo de los valores únicos para un target categórico o numérico discreto.
    umbral_pvalue (float) = valor máximo de pvalue para seleccionar las variables.

    Retorna:
    Lista: devuelve una lista con los nombres de las columnas que cumplen las condiciones.
    """
    
    #Comprobamos que los valores de entrada tienen el tipo correcto
    
    #Comprobamos para el argumento df
    if not(isinstance(df, pd.DataFrame)):
        print("Introduce un DataFrame")
        return None
    
    #Comprobamos para el argumento target_col y umbral_discreta
    if not(isinstance(target_col, str)):
        print("Introduce un string con el nombre del target categórico del DataFrame")
        return None
    
    if target_col not in df.columns.tolist():
        print("Introduce un string con el nombre del target categórico del DataFrame")
        return None
    
    elif not(isinstance(umbral_discreta, (int,float))):
        print("Introduce un valor entero o decimal para el umbral del target categórico")
        return None
    
    elif df[target_col].nunique() > umbral_discreta:
        print("Los valores únicos del target categórico son mayores que el umbral definido")
        return None
    
    #Comprobamos para el argumento umbral_pvalue
    if not(isinstance(umbral_pvalue, (int, float))):
        print("Introduce un valor entero o decimal para el umbral del pvalue y que esté comprendido entre 0.0 y 1.0")
        return None
    
    elif umbral_pvalue < 0 or umbral_pvalue > 1:
        print("Introduce un valor entero o decimal para el umbral del pvalue y que esté comprendido entre 0.0 y 1.0")
        return None
      
    #Creamos una lista con las columnas numericas del DataFrame
    lista_columnas_numericas = []

    for columna in df:        
        try: 
            pd.to_numeric(df[columna], errors='raise')
            lista_columnas_numericas.append(columna) 
            
        except:
            pass
    
    #Comprobamos si se ha incluido el target en la lista (puede ser numérica discreta) para eliminarlo
    if target_col in lista_columnas_numericas:
        lista_columnas_numericas.remove(target_col)

    #Comprobamos si superan el test de correlación
    for columna in lista_columnas_numericas.copy():
        
        #Obtenemos los valores únicos del target categórico
        valores = df[target_col].unique()
        
        #Creamos una lista donde guardar los distintos grupos
        lista_grupos = []
        
        #Separamos los datos en tantos grupos como valores tenga el target categorico
        for valor in valores:
            lista_grupos.append(df.loc[df[target_col] == valor, columna])   
        
        #Calculamos el pvalue y comprobamos su valor
        pvalue = f_oneway(*lista_grupos).pvalue #El operador * lo que hace es separar todos los elementos de la lista y pasarselos como argumento a la función
        
        #Si el pvalue es mayor que el umbral se elimina la columna
        if pvalue > umbral_pvalue:
            lista_columnas_numericas.remove(columna)

    return lista_columnas_numericas  

#############################################################################################################################

#Función plot_features_num_classification (encargado: Rogelio)

def plot_features_num_classification(df, target_col, umbral_discreta=10, lista_columnas=[], umbral_pvalue=0.05, limite_pairplot=5):
    
    """
    Función que genera los gráficos pairplot de las variables (columnas) de un DataFrame que superan el test de relación con confianza estadística dada otra variable target categórica.

    Argumentos:
    df (DataFrame): DataFrame que contiene las variables para las que queremos generar los gráficos pairplot.
    target_col (string): Nombre de la variable del DataFrame considerada como target.
    umbral_discreta (int): valor máximo de los valores únicos para un target categórico o numérico discreto.
    lista_columnas (lista) = Nombres de las columnas del DataFrame para las que queremos generar los gráficos pairplot.
    umbral_pvalue (float) = valor máximo de pvalue para seleccionar las variables.
    limite_pairplot (int) = valor máximo de variables a generar en los gráficos pairplot.

    Retorna:
    Lista: devuelve una lista con los nombres de las columnas numéricas que cumplen las condiciones.
    """
    
    #Comprobamos que los valores de entrada tienen el tipo correcto
    
    #Comprobamos para el argumento df
    if not(isinstance(df, pd.DataFrame)):
        print("Introduce un DataFrame")
        return None
    
    #Comprobamos para el argumento target_col y umbral_discreta
    if not(isinstance(target_col, str)):
        print("Introduce un string con el nombre del target categórico del DataFrame")
        return None
    
    if target_col not in df.columns.tolist():
        print("Introduce un string con el nombre del target categórico del DataFrame")
        return None
    
    elif not(isinstance(umbral_discreta, (int,float))):
        print("Introduce un valor entero o decimal para el umbral del target categórico")
        return None
    
    elif df[target_col].nunique() > umbral_discreta:
        print("Los valores únicos del target categórico son mayores que el umbral definido")
        return None
    
    #Comprobamos para el argumento lista_columnas
    if not(isinstance(lista_columnas, list)):
        print("Introduce una lista con los nombres de las columnas del DataFrame a analizar")
        return None
    
    for columna in lista_columnas:
        if columna == target_col:
            print("Se ha introducido una lista que incluye la columna target del DataFrame a analizar")
            return None

        if columna not in df.columns.tolist():
            print("Se ha introducido una lista con columnas que no pertenecen al DataFrame a analizar")
            return None
    
    #Comprobamos para el argumento umbral_pvalue
    if not(isinstance(umbral_pvalue, (int, float))):
        print("Introduce un valor entero o decimal para el umbral del pvalue y que esté comprendido entre 0.0 y 1.0")
        return None
    
    elif umbral_pvalue < 0 or umbral_pvalue > 1:
        print("Introduce un valor entero o decimal para el umbral del pvalue y que esté comprendido entre 0.0 y 1.0")
        return None

    #Comprobamos para el argumento limite_pairplot
    if not(isinstance(limite_pairplot, int)):
        print("Introduce un valor entero con el límite de variables a representar en el pairplot")
        return None

    elif limite_pairplot < 2:
        print("El valor introducido debe ser mayor o igual a 2")
        return None
    
    #Comprobamos la lista de columnas a analizar
    if lista_columnas == []:
        columnas_analizar = df.columns.tolist()
    
    else:
        columnas_analizar = lista_columnas
    
    #Creamos una lista con las columnas numericas del DataFrame de entre las que vamos a analizar
    lista_columnas_numericas = []

    for columna in columnas_analizar:        
        try: 
            pd.to_numeric(df[columna], errors='raise')
            lista_columnas_numericas.append(columna) 
            
        except:
            pass
    
    #Comprobamos si se ha incluido el target en la lista (puede ser numérica discreta) para eliminarlo
    if target_col in lista_columnas_numericas:
        lista_columnas_numericas.remove(target_col)
    
    #Comprobamos si superan el test de correlación
    for columna in lista_columnas_numericas.copy():
        
        #Obtenemos los valores únicos del target categórico
        valores = df[target_col].unique()
        
        #Creamos una lista donde guardar los distintos grupos
        lista_grupos = []
        
        #Separamos los datos en tantos grupos como valores tenga el target categorico
        for valor in valores:
            lista_grupos.append(df.loc[df[target_col] == valor, columna])   
        
        #Calculamos el pvalue y comprobamos su valor
        pvalue = f_oneway(*lista_grupos).pvalue #El operador * lo que hace es separar todos los elementos de la lista y pasarselos como argumento a la función
        
        #Si el pvalue es mayor que el umbral se elimina la columna
        if pvalue > umbral_pvalue:
            lista_columnas_numericas.remove(columna)
    
    #Calculamos cuántos gráficos hay que generar
    num_graficos = (len(lista_columnas_numericas) // (limite_pairplot))
    
    if len(lista_columnas_numericas) % (limite_pairplot) != 0:
        num_graficos = num_graficos + 1

    #Generamos los gráficos
    if num_graficos == 1:
    
        lista = lista_columnas_numericas.copy()
        lista.append(target_col)
    
        sns.pairplot(df[lista], hue=target_col, palette="viridis", height=3, aspect=1.5)

    else:
        
        for i in range(0,num_graficos):
            
            #Creamos listas con las distintas columnas a relacionar con el target
            lista = lista_columnas_numericas[(limite_pairplot)*i:(limite_pairplot)*i+(limite_pairplot)].copy()
            lista.append(target_col)
            
            sns.pairplot(df[lista], hue=target_col, palette="viridis", height=2, aspect=1.5)

    return lista_columnas_numericas 

#############################################################################################################################

#Función get_features_cat_classification (encargado: Estela)

def get_features_cat_classification(df, target_col, normalize=False, mi_threshold=0):
    """
    Devuelve una lista de variables categóricas basado en la información mutua con el target.

    Argumentos:
        df: dataframe.
        target_col (str): nombre del target (variable categórica).
        normalize (bool): su valor por defecto es False.
        mi_threshold (float): umbral de información mutua cuyo valor por defecto es 0.

    Devuelve:
        lista: lista de las variables categóricas.
    """
    #Comprobamos si el target existe en el dataframe
    if target_col not in df.columns: #si el target no está en las columnas del dataframe
        print("Error: ", target_col, "no es una columna del dataframe.") #imprime un error
        return None #devuelve none

    #Comprobamos si el target es una variable categórica
    if not pd.api.types.is_categorical_dtype(df[target_col]): #función que tiene como argumento el target y verifica si es categórica o no
        #si no es una variable categórica
        print("Error: ", target_col, "no es una variable categórica.") #imprime un error
        return None #devuelve none

    #Calculamos la información mutua entre las variables (excepto el target) y el target.
    mi_values = mutual_info_classif(df.drop(columns=[target_col]), df[target_col], discrete_features=True) #discrete_features=True indica que las variables son categóricas

    #Normalizamos la información mutua
    if normalize: #si normalizamos devuelve una lista con las variables categóricas cuyo valor normalizado de información mutua con el target iguale o supere el valor del umbral de información mutua
        total_mi = sum(mi_values) #calculamos la suma total de los valores de información mutua
        mi_values = [mi / total_mi for mi in mi_values] #normalizamos cada valor de información mutua dividiéndolo por el total

        #Comprobamos si el umbral de información mutua es un float entre 0 y 1
        if not (0 <= mi_threshold <= 1): #si el umbral no está entre 0 y 1
            print("Error: 'mi_threshold' no está entre 0 y 1.") #imprime un error
            return None #devuelve none

    #Creamos una lista de variables categóricas basada en el umbral de información mutua (mi_threshold)
    selected_features = [col for col, mi in zip(df.drop(columns=[target_col]).columns, mi_values) if mi >= mi_threshold]
    #zip(df.drop(columns=[target_col]).columns, mi_values -> combina las variables (excepto el target) con los valores de información mutua
    #para cada par de variable y valor de información mutua: si el valor de información mutua es mayor o igual que el umbral, agrega el nombre de la variable a la lista 

    return selected_features #devuelve la lista de variables categóricas

#############################################################################################################################

#Función plot_features_cat_classification (encargado: Numa)
    
def plot_features_cat_classification():
    
    """
    Realiza XXX

    Argumentos:
    XXXX

    Retorna:
    XXX
    """
    
    return None

#############################################################################################################################


