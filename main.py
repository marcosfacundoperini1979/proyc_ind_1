from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import pyarrow.parquet as pq
import numpy as np

app = FastAPI()

df1 = pd.read_csv('steamgames_final.csv')
#df2 = pd.read_csv(r'C:\python\proyectohenry\data\user_items_final2.csv')



# Lista para almacenar cada DataFrame
dataframes = []

# Cargar cada archivo CSV en un DataFrame y añadirlo a la lista
for i in range(10):
    df_i = pd.read_csv(f'parte_{i}.csv')
    dataframes.append(df_i)

# Unir todos los DataFrames en uno solo
df2 = pd.concat(dataframes)






df3 = pd.read_csv('user_reviews_final.csv')






@app.get("/playtime_genre/{genero}")
def playtime_genre(genero: str):
    juegos_genero = df1[df1[genero] == 1]

    df = pd.merge(juegos_genero, df2, left_on='id', right_on='item_id')

    df_grouped = df.groupby('year')['playtime_forever'].sum().sort_values(ascending=False)

    year_max_playtime = df_grouped.idxmax()

    return {f"Año de lanzamiento con más horas jugadas para {genero}" : int(year_max_playtime)}


@app.get("/user_for_genre/{genero}")
def user_for_genre(genero: str):
    juegos_genero = df1[df1[genero] == 1]

    df = pd.merge(juegos_genero, df2, left_on='id', right_on='item_id')

    df_grouped = df.groupby('user_id')['playtime_forever'].sum().sort_values(ascending=False)

    user_max_playtime = df_grouped.idxmax()

    df_grouped_year = df.groupby(['year', 'user_id'])['playtime_forever'].sum().reset_index()

    playtime_by_year = df_grouped_year[df_grouped_year['user_id'] == user_max_playtime]

    return {"Usuario con más horas jugadas para el género {genero}": user_max_playtime, "Acumulación de horas jugadas por año": playtime_by_year.to_dict(orient='records')}

@app.get("/users_recommend/{year}")
def users_recommend(year: int):
    # Filtra df3 para obtener solo las reseñas del año especificado que son positivas/neutrales y que recomiendan el juego
    reseñas_año = df3[(df3['recommend'] == True) & (df3['sentiment'].isin(['buena', 'neutral'])) & (df3['year'] == year)]

    # Si no hay reseñas para el año especificado, devuelve un mensaje específico
    if reseñas_año.empty:
        return {"Mensaje": "No hay datos para el año {}".format(year)}

    # Agrupa por 'item_id' y cuenta las reseñas, luego ordena los resultados
    df_grouped = reseñas_año.groupby('item_id').size().sort_values(ascending=False)

    # Obtiene los IDs de los tres juegos con más reseñas
    top_juegos_ids = df_grouped.nlargest(3).index.tolist()

    # Obtiene los nombres de los juegos a partir de los IDs
    top_juegos_nombres = df1[df1['id'].isin(top_juegos_ids)]['title'].tolist()

    # Crea una lista de diccionarios para el resultado
    resultado = [{"Puesto {}".format(i+1) : nombre} for i, nombre in enumerate(top_juegos_nombres)]

    return resultado

@app.get("/users_worst_developer/{year}")
def users_worst_developer(year: int):
    # Filtra df3 para obtener solo las reseñas del año especificado que son negativas y que no recomiendan el juego
    reseñas_año = df3[(df3['recommend'] == False) & (df3['sentiment'] == 'mala') & (df3['year'] == year)]

    # Si no hay reseñas negativas para el año especificado, devuelve un mensaje específico
    if reseñas_año.empty:
        return {"Mensaje": "No hay reseñas negativas para el año {}".format(year)}

    # Une df1 (información del juego) con reseñas_año en 'item_id'
    df = pd.merge(df1, reseñas_año, left_on='id', right_on='item_id')

    # Agrupa por 'developer' y cuenta las reseñas, luego ordena los resultados
    df_grouped = df.groupby('developer').size().sort_values(ascending=True)

    # Obtiene los nombres de las tres desarrolladoras con más reseñas negativas
    worst_developers = df_grouped.nsmallest(3).index.tolist()

    # Crea una lista de diccionarios para el resultado
    resultado = [{"Puesto {}".format(i+1) : nombre} for i, nombre in enumerate(worst_developers)]

    return resultado

@app.get("/sentiment_analysis/{empresa_desarrolladora}")
def sentiment_analysis(empresa_desarrolladora: str):
    # Filtra df1 para obtener solo los juegos de la empresa desarrolladora especificada
    juegos_empresa = df1[df1['developer'] == empresa_desarrolladora]

    # Une df3 (reseñas) con juegos_empresa en 'id'
    df = pd.merge(juegos_empresa, df3, left_on='id', right_on='item_id')

    # Cuenta las reseñas por sentimiento
    conteo_sentimientos = df['sentiment'].value_counts().to_dict()

    # Crea un diccionario para el resultado
    resultado = {empresa_desarrolladora : conteo_sentimientos}

    return resultado

@app.get("/recomendacion_juego/{id_producto}")
def recomendacion_juego(id_producto: int):
    # Asegúrate de que el ID de producto existe en df1
    if id_producto not in df1['id'].values:
        return {"Mensaje": "No se encontró el juego con el ID de producto {}".format(id_producto)}

    # Selecciona las columnas numéricas de df1
    columnas_numericas = df1.select_dtypes(include=['number'])

    # Normaliza las columnas numéricas
    scaler = StandardScaler()
    columnas_numericas_normalizadas = pd.DataFrame(scaler.fit_transform(columnas_numericas), columns=columnas_numericas.columns, index=df1.index)

    # Calcula la matriz de similitud del coseno
    similarity_matrix = cosine_similarity(columnas_numericas_normalizadas)

    # Crea un DataFrame de similitud con los ID de los juegos como índice y columnas
    df_similarity = pd.DataFrame(similarity_matrix, index=df1['id'], columns=df1['id'])

    # Obtén la fila correspondiente al juego de referencia
    game_row = df_similarity.loc[id_producto]

    # Ordena la fila por similitud del coseno descendente y selecciona los juegos más similares
    similar_games = game_row.sort_values(ascending=False).index[1:6]

    # Obtiene los nombres de los juegos usando los ID
    similar_games_titles = df1[df1['id'].isin(similar_games)]['title'].tolist()

    return {df1[df1['id'] == id_producto]['title'].values[0]: similar_games_titles}
