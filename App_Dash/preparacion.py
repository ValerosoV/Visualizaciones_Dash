from model import Database
from model import Cargue
import pandas as pd

#ejecutar este archivo cuando no exista una Base de Datos en la carpeta raiz del proyecto

#llamo al constructor de la clase DATABASE() para crea la DB con asignando snies.db como el parametro: nombre_base_datos
base_datos = Database('snies.db')

base_datos.create_table_programa()  #
base_datos.create_table_sexo()      #Estos tres para crear las respectivas tablas de la DB
base_datos.create_table_snies_fact()# 

carga = Cargue()        ##llamo a la clae Cargue() del Archivo Modelo para que use la Libreria de Pandas como le indicamos

#definIMOS con que datos trabajaremos:
institucion = [2712]    #Codigo de la Institucion de la Konrad
lv_formacion = [1]      #El valor para los programas academicos de pregrados
 
#use el metodo cargue_archivo de la Clase Carga del arhivo modelo para crear el df corespondiente
df_admitidos_2023 = carga.cargue_archivo(nombre_archivo='Admitidos2023.xlsx',hoja=1, encabezado=5, codigo_institucion=institucion, nivel_formacion = lv_formacion)
df_graduados_2023 = carga.cargue_archivo(nombre_archivo='Graduados2023.xlsx',hoja=1, encabezado=5, codigo_institucion=institucion, nivel_formacion = lv_formacion)

#usando las columna dadas, ejecute el metodo insert_programa y llene los registros unicos que se añadiran en la tabla PROGRAMA
print('#####Esto otro es lo que tiene el df de los ADMITIDOS2023 tras que se acabe el metodo: cargue_archivo')
print(df_admitidos_2023)

columnas_programa = ['CÓDIGO SNIES DEL PROGRAMA', 'PROGRAMA ACADÉMICO']
base_datos.insert_programa(df_admitidos_2023,columnas_programa)
 
#usando las columna dadas, ejecute el metodo insert_sexo y llene los registros unicos que se añadiran en la tabla SEXO
print('#####Esto otro es lo que tiene el df de los ADMITIDOS2023 tras que se acabe el metodo: cargue_archivo')
print(df_admitidos_2023)

columnas_sexo = ['ID SEXO', 'SEXO']
base_datos.insert_sexo(df_admitidos_2023,columnas_sexo)
 
#sentencias para crear la tabla FACT:

##definimos las columnas clave para ambos archivos .XLSX, luego filtramos solo esas columnas que nos son utiles
columnas_admitidos = ['CÓDIGO DE LA INSTITUCIÓN','CÓDIGO SNIES DEL PROGRAMA','ID SEXO','AÑO','SEMESTRE','ADMITIDOS']
df_admitidos_2023 = df_admitidos_2023[columnas_admitidos]

columnas_graduados = ['CÓDIGO DE LA INSTITUCIÓN','CÓDIGO SNIES DEL PROGRAMA','ID SEXO','AÑO','SEMESTRE','GRADUADOS']
df_graduados_2023 = df_graduados_2023[columnas_graduados]
 
##definimos las columnas que tienen en comun
columnas_clave = ['CÓDIGO DE LA INSTITUCIÓN','CÓDIGO SNIES DEL PROGRAMA','ID SEXO','AÑO','SEMESTRE']
 
##hacemos el merge de ambos df y aseguramos que sus columnas manejen con INTS  
df_fact = pd.merge(df_admitidos_2023, df_graduados_2023, on=columnas_clave, how='inner')
df_fact['GRADUADOS'] = df_fact['GRADUADOS'].astype(int)
df_fact['ADMITIDOS'] = df_fact['ADMITIDOS'].astype(int)
df_fact['ID SEXO'] = df_fact['ID SEXO'].astype(int)
df_fact['AÑO'] = df_fact['AÑO'].astype(int)
df_fact['SEMESTRE'] = df_fact['SEMESTRE'].astype(int)
df_fact['CÓDIGO SNIES DEL PROGRAMA'] = df_fact['CÓDIGO SNIES DEL PROGRAMA'].astype(int)

#muestre en consola como quedo la estructura del DF
print(df_fact) 
base_datos.insert_snies_fact(df=df_fact,columnas=df_fact.columns)
