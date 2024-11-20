import sqlite3
import pandas as pd

class Database:                             #Crear la clase Modelo
    def __init__(self, nombre_base_datos):              #funcion Constructor de la Clase
        self.conn = sqlite3.connect(nombre_base_datos)      #crear la coneccion con la base de Datos
        self.cursor = self.conn.cursor()                    #crear un cursor para que envie los Querys a la base de datos
    
    #Metodo de Crear la tabla programa: en la DB (id, nombre),
    # campos de XLSX dados en preparacion.py :('CÓDIGO SNIES DEL PROGRAMA', 'PROGRAMA ACADÉMICO')
    def create_table_programa(self):
        #Query a Ejecutar
        self.cursor.execute('''    
            CREATE TABLE IF NOT EXISTS PROGRAMA (
                            ID INTEGER PRIMARY KEY,
                            NOMBRE TEXT NOT NULL UNIQUE
                            )
                            ''')
        self.conn.commit() #usando la conexión que envie el Query y se ejecute
    
    #Metodo de Crear la tabla SEXO: en la DB (id, nombre),
    # campos de XLSX dados en preparacion.py :(ID SEXO, SEXO)
    def create_table_sexo(self):   
        #Query   
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SEXO (
                            ID INTEGER PRIMARY KEY,
                            NOMBRE TEXT NOT NULL UNIQUE
                            )
                            ''')
        self.conn.commit()

    #Metodo de Crear la tabla SNIES_FACT: en la DB,
    #campos respectivos del .XLSX :(pos el id no tiene contraparte, CÓDIGO DE LA INSTITUCIÓN, CÓDIGO SNIES DEL PROGRAMA, ID SEXO, AÑO, SEMESTRE, ADMITIDOS, GRADUADOS)
    def create_table_snies_fact(self):  #
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SNIES_FACT(
                            ID INTEGER PRIMARY KEY,
                            ID_INSTITUCION INTEGER,                            
                            ID_PROGRAMA INTEGER,
                            ID_SEXO INTEGER,
                            ANIO INTEGER,
                            SEMESTRE INTEGER,    
                            ADMITIDOS INTEGER,                        
                            GRADUADOS INTEGER,                            
                            CONSTRAINT fk_sexo FOREIGN KEY (ID_SEXO) REFERENCES SEXO(ID),
                            CONSTRAINT fk_programa FOREIGN KEY (ID_PROGRAMA) REFERENCES PROGRAMA(ID)
                            )
                            ''')
        self.conn.commit()

    #Funcion Python que usa el dataframe otorgado y las columnas para operar con la 
    #libreria Pandas para hacer la insercion de datos en la respectiva Tabla de la DB
    def insert_programa(self, df,columnas):
        print('#####Se entro al Insert de Programa, vea el head:')
        print(df.head())                ##LE esta llegando Vacio, o sea sin registros
        print('***vea las columnas')
        print(df.columns)

        df = df[columnas].drop_duplicates()              #tome el df, filtre las columnas dadas con cada registro UNICO
        print('se dropearon los duplicados, y el df quedo como:')
        print(df.head())

        df[columnas[0]] = df[columnas[0]].astype(int)    #que la primera columna (la llave primaria: el ID) use datos de tipo INT

        #renombre las como se le indica: 'CÓDIGO SNIES DEL PROGRAMA', 'PROGRAMA ACADÉMICO' pasan a ser 'ID', 'NOMBRE'
        df.rename(columns={columnas[0]: 'ID', columnas[1]: 'NOMBRE'}, inplace=True) 

        #transforme el dataframe a una sentencia SQL, para la tabla Programa, de la base indicada en la conexión, 
        #creando nuevos Registros/Filas con los datos dados y sin usar el index de Panda como otra columna
        df.to_sql('PROGRAMA', self.conn, if_exists='append', index=False)
        self.conn.commit()                               #por medio de la Conexion ejecute lo que se indico en la BD
    
    def insert_sexo(self, df,columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)

        #renombre las columnas del Dataframe como se le indica: 'ID SEXO', 'SEXO' pasan a ser: 'ID', 'NOMBRE'
        df.rename(columns={columnas[0]: 'ID', columnas[1]: 'NOMBRE'}, inplace=True) 
 
        df.to_sql('SEXO', self.conn, if_exists='append', index=False)
        self.conn.commit()

    def insert_snies_fact(self, df,columnas):
        #renombre las columnas del df dado (en preparacion se otorgan las del un Merge entre admititdos y graduados con la forma):
        #1'CÓDIGO DE LA INSTITUCIÓN',2'CÓDIGO SNIES DEL PROGRAMA',3'ID SEXO',4'AÑO',5'SEMESTRE',6'ADMITIDOS',7'GRADUADOS'
        #como:
        #1'ID_INSTITUCION',2'ID_PROGRAMA',3'ID_SEXO',4'ANIO',5'SEMESTRE',6'ADMITIDOS',7'GRADUADOS'        
        df.rename(columns={columnas[0]: 'ID_INSTITUCION', columnas[1]: 'ID_PROGRAMA', columnas[2]: 'ID_SEXO', columnas[3]: 'ANIO', columnas[4]: 'SEMESTRE', columnas[5]: 'ADMITIDOS', columnas[6]: 'GRADUADOS'}, inplace=True)     

        df.to_sql('SNIES_FACT', self.conn, if_exists='append', index=False)
        self.conn.commit()


class Cargue:       #Crear una clase llamada Cargue la cual:

    #reciba nombre del archivo, el nombre la hoja, las lineas que saltar y LA institucion por filtrar
    def cargue_archivo(self, nombre_archivo, hoja, encabezado, codigo_institucion,nivel_formacion): 
        df = pd.read_excel(nombre_archivo, sheet_name=hoja, header=encabezado)  #lee los datos del archivo mecionado, en la hoja dada, empezando desde la linea indicada
        df = df[df['CÓDIGO DE LA INSTITUCIÓN'].isin(codigo_institucion)]        #luego los filtra por institucion
        df = df[df['ID NIVEL ACADÉMICO'].isin(nivel_formacion)]                 #luego los filtre para que sean solo Pregrados o posgrados como se le indique
        return df