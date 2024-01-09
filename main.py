from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import pyarrow.parquet as pq
import numpy as np

app = FastAPI()



#carga de datos

df1 = pd.read_csv('steamgames_final.csv')
#df2 = pd.read_csv(r'C:\python\proyectohenry\data\user_items_final2.csv')
dataframes = []
# Cargar cada archivo CSV en u n Df y lo uno
for i in range(10):
    df_i = pd.read_csv(f'parte_{i}.csv')
    dataframes.append(df_i)
df2 = pd.concat(dataframes)
df3 = pd.read_csv('user_reviews_final.csv')

#endpoint1

@app.get("/playtime_genre/{genero}")
def playtime_genre(genero: str):
    juegos_genero = df1[df1[genero] == 1]
    df = pd.merge(juegos_genero, df2, left_on='id', right_on='item_id')
    df_grouped = df.groupby('year')['playtime_forever'].sum().sort_values(ascending=False)
    year_max_playtime = df_grouped.idxmax()
    return {f"Año de lanzamiento con más horas jugadas para {genero}" : int(year_max_playtime)}

#endpoint2

@app.get("/user_for_genre/{genero}")
def user_for_genre(genero: str):
    juegos_genero = df1[df1[genero] == 1]
    df = pd.merge(juegos_genero, df2, left_on='id', right_on='item_id')
    df_grouped = df.groupby('user_id')['playtime_forever'].sum().sort_values(ascending=False)
    user_max_playtime = df_grouped.idxmax()
    df_grouped_year = df.groupby(['year', 'user_id'])['playtime_forever'].sum().reset_index()
    playtime_by_year = df_grouped_year[df_grouped_year['user_id'] == user_max_playtime]
    return {"Usuario con más horas jugadas para el género {genero}": user_max_playtime, "Acumulación de horas jugadas por año": playtime_by_year.to_dict(orient='records')}

#endpoint3

@app.get("/users_recommend/{year}")
def users_recommend(year: int):
    reseñas_año = df3[(df3['recommend'] == True) & (df3['sentiment'].isin(['buena', 'neutral'])) & (df3['year'] == year)]
    if reseñas_año.empty:
        return {"Mensaje": "No hay datos para el año {}".format(year)}
    df_grouped = reseñas_año.groupby('item_id').size().sort_values(ascending=False)
    top_juegos_ids = df_grouped.nlargest(3).index.tolist()
    top_juegos_nombres = df1[df1['id'].isin(top_juegos_ids)]['title'].tolist()
    resultado = [{"Puesto {}".format(i+1) : nombre} for i, nombre in enumerate(top_juegos_nombres)]
    return resultado

#endpoint4

@app.get("/users_worst_developer/{year}")
def users_worst_developer(year: int):
    reseñas_año = df3[(df3['recommend'] == False) & (df3['sentiment'] == 'mala') & (df3['year'] == year)]
    if reseñas_año.empty:
        return {"Mensaje": "No hay reseñas negativas para el año {}".format(year)}
    df = pd.merge(df1, reseñas_año, left_on='id', right_on='item_id')
    df_grouped = df.groupby('developer').size().sort_values(ascending=True)
    worst_developers = df_grouped.nsmallest(3).index.tolist()
    # Crea una lista de diccionarios para el resultado
    resultado = [{"Puesto {}".format(i+1) : nombre} for i, nombre in enumerate(worst_developers)]
    return resultado

#endpoint5

@app.get("/sentiment_analysis/{empresa_desarrolladora}")
def sentiment_analysis(empresa_desarrolladora: str):
    juegos_empresa = df1[df1['developer'] == empresa_desarrolladora]
    df = pd.merge(juegos_empresa, df3, left_on='id', right_on='item_id')
    conteo_sentimientos = df['sentiment'].value_counts().to_dict()
    resultado = {empresa_desarrolladora : conteo_sentimientos}
    return resultado

#endpoint6

@app.get("/recomendacion_juego/{id_producto}")
def recomendacion_juego(id_producto: int):
    if id_producto not in df1['id'].values:
        return {"Mensaje": "No se encontró el juego con el ID de producto {}".format(id_producto)}
    columnas_numericas = df1.select_dtypes(include=['number'])
    scaler = StandardScaler()
    columnas_numericas_normalizadas = pd.DataFrame(scaler.fit_transform(columnas_numericas), columns=columnas_numericas.columns, index=df1.index)
    similarity_matrix = cosine_similarity(columnas_numericas_normalizadas)
    df_similarity = pd.DataFrame(similarity_matrix, index=df1['id'], columns=df1['id'])
    game_row = df_similarity.loc[id_producto]
    similar_games = game_row.sort_values(ascending=False).index[1:6]
    similar_games_titles = df1[df1['id'].isin(similar_games)]['title'].tolist()

    return {df1[df1['id'] == id_producto]['title'].values[0]: similar_games_titles}
