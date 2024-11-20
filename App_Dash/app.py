import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import plotly.express as px
 
#Conexion al gestor base de datos sqlite3
conn = sqlite3.connect('snies.db', check_same_thread=False) #conectese a la base snies.db
 
def programa_dropdown():
    df_programa = pd.read_sql_query("SELECT * FROM PROGRAMA", conn)
    options = [{"label": nombre, "value": id} for id, nombre in zip(df_programa["ID"], df_programa["NOMBRE"])]
    # Agregar una opción adicional para 'Todas'
    options.insert(0, {"label": "Todas", "value": 0})
    return options
 
def semestre_dropdown():
    options = [
        {"label": "Primer Semestre", "value": 1},
        {"label": "Segundo Semestre", "value": 2},
        {"label": "Año Entero", "value": 0}  # Opción predeterminada
    ]
    return options
 
def grafico_barras(programa=0, semestre=0):

    #Escoja un Query segun las opciones seleccionadas del DropDown

    if programa == 0 and semestre == 0:             #Si no se ha elegido ni Programa ni Semestre
        consulta = '''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            GROUP BY PROGRAMA.NOMBRE
        '''
    elif programa != 0 and semestre == 0:           #Si no se ha elegido Semestre PERO si un Programa
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            WHERE PROGRAMA.ID = {programa}
            GROUP BY PROGRAMA.NOMBRE
        '''
    elif programa == 0 and semestre != 0:           #Si no se ha elegido Programa PERO si un Semestre
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            WHERE SNIES_FACT.SEMESTRE = {semestre}
            GROUP BY PROGRAMA.NOMBRE
        '''
    else:                                           #Si se eligio tanto un Programa como un Semestre
        consulta = f''' 
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            WHERE PROGRAMA.ID = {programa} AND SNIES_FACT.SEMESTRE = {semestre}
            GROUP BY PROGRAMA.NOMBRE
        '''

    #luego del If anidado, creeme un DataFrame con la consulta resultante    
    df_snies_fact1 = pd.read_sql_query(consulta, conn)
 
    # Transformar los datos para Plotly
    df_plot = df_snies_fact1.melt(id_vars=["PROGRAMA"], value_vars=["ADMITIDOS", "GRADUADOS"],
                                          var_name="Categoría1", value_name="Total1")

    # Crear el gráfico de barras agrupadas con Plotly Express
    fig1 = px.bar(
        df_plot,
        x="PROGRAMA",
        y="Total1",
        color="Categoría1",
        barmode="group",
        title="Comparación de Admitidos y graduados por Programa",
        labels={"Total": "Número de Estudiantes", "PROGRAMA": "Programa"}
    )
    return fig1
 
#### GRAFICO DE PASTEL Amitidos #1
 
def grafico_pastel_1(programa=0, semestre=0):
    if programa == 0 and semestre == 0:
        consulta = '''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            GROUP BY PROGRAMA.NOMBRE
        '''
    elif programa != 0 and semestre == 0:
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID            
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            WHERE PROGRAMA.ID = {programa}
            GROUP BY PROGRAMA.NOMBRE, SNIES_FACT.ID_SEXO, SEXO.NOMBRE
        '''
    elif programa == 0 and semestre != 0:
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            WHERE SNIES_FACT.SEMESTRE = {semestre}
            GROUP BY PROGRAMA.NOMBRE
        '''
    else:
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID            
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            WHERE PROGRAMA.ID = {programa} AND SNIES_FACT.SEMESTRE = {semestre}
            GROUP BY PROGRAMA.NOMBRE, SNIES_FACT.ID_SEXO, SEXO.NOMBRE
        '''
 
    #luego del If anidado, creeme un DataFrame con la consulta resultante    
    df_snies_fact2 = pd.read_sql_query(consulta, conn)
 
    # Transformar los datos para Plotly
    #df_plot2 = df_snies_fact2.melt(id_vars=["PROGRAMA"], value_vars=["ADMITIDOS"],var_name="Categoría2", value_name="Total2")

    #Cree el Grafico de Pastel para los ADMITIDOS
    fig2 = px.pie(
        df_snies_fact2,
        values='ADMITIDOS',
        names='GENERO',
        title='Distribución de Admitidos por Sexo'
    )
    return fig2

    #### GRAFICO DE PASTEL Graduados #2
 
def grafico_pastel_2(programa=0, semestre=0):
    if programa == 0 and semestre == 0:
        consulta = '''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            GROUP BY PROGRAMA.NOMBRE
        '''
    elif programa != 0 and semestre == 0:
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID            
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            WHERE PROGRAMA.ID = {programa}
            GROUP BY PROGRAMA.NOMBRE, SNIES_FACT.ID_SEXO, SEXO.NOMBRE
        '''
    elif programa == 0 and semestre != 0:
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID            
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            WHERE SNIES_FACT.SEMESTRE = {semestre}
            GROUP BY PROGRAMA.NOMBRE
        '''
    else:
        consulta = f'''
            SELECT
                PROGRAMA.NOMBRE AS PROGRAMA,
                SNIES_FACT.ID_SEXO AS SEXO,
                SEXO.NOMBRE AS GENERO,
                SUM(SNIES_FACT.GRADUADOS) AS GRADUADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID            
            INNER JOIN SEXO on SNIES_FACT.ID_SEXO = SEXO.ID 
            WHERE PROGRAMA.ID = {programa} AND SNIES_FACT.SEMESTRE = {semestre}
            GROUP BY PROGRAMA.NOMBRE, SNIES_FACT.ID_SEXO, SEXO.NOMBRE
        '''
 
    #luego del If anidado, creeme un DataFrame con la consulta resultante    
    df_snies_fact3 = pd.read_sql_query(consulta, conn)
 
    # Transformar los datos para Plotly
    #df_plot3 = df_snies_fact3.melt(id_vars=["PROGRAMA"], value_vars=["ADMITIDOS"],var_name="Categoría2", value_name="Total2")

    #Cree el Grafico de Pastel para los ADMITIDOS
    fig2 = px.pie(
        df_snies_fact3,
        values='GRADUADOS',
        names='GENERO',
        title='Distribución de Graduados por Sexo'
    )
    return fig2
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
 
app.layout = html.Div([
    html.H1("Proyecto Dashboard Interactivo SNIES"),
    html.H2("Hecho por: Juan David Valero Vanegas 506221052, David Alejandro Hernandez Melendez "),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Label("Programa"),
            dcc.Dropdown(
                            id='programa_dropdown',
                            options=programa_dropdown(),
                            value=0
                        )
            ]),
        dbc.Col([
            html.Label("Semestre"),
            dcc.Dropdown(
                            id='semestre_dropdown',
                            options=semestre_dropdown(),
                            value=0
                        )
            ]),
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico_barras', figure=grafico_barras())
        ])
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id='grafico_de_pastel_1', figure=grafico_pastel_1())
        ])
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id='grafico_de_pastel_2', figure=grafico_pastel_2())
        ])
    ]),
])
 
@app.callback(
    Output(component_id='grafico_barras', component_property='figure'),
    Output(component_id='grafico_de_pastel_1', component_property='figure'),
    Output(component_id='grafico_de_pastel_2', component_property='figure'),
    [Input(component_id= 'programa_dropdown', component_property='value'),
    Input(component_id='semestre_dropdown', component_property='value')]
)
def update_graph(programa, semestre):
    return grafico_barras(programa, semestre),grafico_pastel_1(programa, semestre),grafico_pastel_2(programa, semestre)
 
 
if __name__ == '__main__':
    app.run_server(debug=True)
