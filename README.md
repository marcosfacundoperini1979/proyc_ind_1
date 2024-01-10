<div style="background-color:black;color:white;padding:20px;">
# Proyecto individal -- Machine Learning

## Detalle del proyecto 🚀
El Proyecto consta de varias partes muy interesantes........
*ETL de un archivo grande el cual no se porque, lo abria y me daba mas del 70% de los datos corruptos, siendo minucioso como lo soy
 esto no me lo podía permitir, asi que edite el mismo usando Notepad++ que permite reemplazar buscando Expresiones regulares...
 Me llevo limpiar ee CSV casi 3 dias para luego interpretar que no podia Hacer unETL Ya que mi pc estallaba cuando Trate de  guardarlo en un archivo
 A pesar de limpiar eliminiar columnas datos duplicados.... etc.
 Se me ocurrio utilizar Pyspark, volaba mi pc  y el proceso de ETL se haci maravilloso.... hasta que intente escribir los datos  a un archivo el cual me Explotaba la pc.
 Ultimo recuro y a  tan solo 3 dias del Deadline    recorde  el hermoso mundo de Databrics la edicion freee community edition.....  y es donde pude relizar el primer etl
 y convertir  esos archivos en Dataframe reutilizabke por mi limitada PC,,,
 EDA fue para el ultimo contacto  de trabajo con  mis archivos Yaque teniamos que lograr Armar Una API con Varios END POINTs


*FastAPi, Toco Armar Api con los siguientes endpoints

Desarrollo API: Propones disponibilizar los datos de la empresa usando el framework FastAPI. Las consultas que propones son las siguientes:

Debes crear las siguientes funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).

def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

*def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

*def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

*def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
---Este endpoint es uno de los que mas me gusto me dio la posibilidad de usar TextBlob.. lohabia hecho en Pyspark  con todo lo potente que es pero por algun
---motivo aparecio un error de consola  en err4j que luego de mucho esfuerzo es por falta de rendimiento de la pc   en un momento funcionaba utilizando las Funcions UDF pero
-- dejo de hacerlo y recurri a nuestro gran amigo pandas y   pude resolverlo mediante ayudin de databrics quien me permitia trabajar con los datos!!!!!


y la parte de Aprendizaje y seleccion fuaaaa lo que me costo 

Si es un sistema de recomendación item-item:

def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
Utilizando el sistema de similitud porr coseno Preprocesando los items normalizando y esclando y convirtiendo a variables Dummies Todo este proceso realizado
en Pandas luego de haber Achicado mi archivo un monton!!!!!!!!
Mi pc dejo de correrlo en Fast Api    solo  veo la recomendacion pura y dura  en un archivo en notebook  ya que cuando intento ejecutar  la fast api local con el sistema de recomendacion explota la pc y recurro al hard reset XDDDD
pero pude probar la fast api en otra pc y el codigo funciona correctamente

---por ultimo el deployment 
     --- [https://marcos-perini-api.onrender.com/docs](https://marcos-perini-api.onrender.com/docs) 
  ---  
   con mucho trabajo y nueva tecnologia que desconocia aprendi hacer un deployment de mi api  la cual funcionan de los 6 end points 3  los otros 3  se queda sin recursos la
   maquina virtual que me manda mails y lo mejor que ya no es mi pc...
       #*--- lo cual vern con el video que si funciona mi codigo ---*

       
 ## descripcion de filas 🛠️
 directorio etl archivos notebooks que me dieron lscsv finales para hacer el deploy
 veran que hay 10 archivos que los divide asi para luego joinearlos en el deploy para usar un solo archivo y evadir a github que no te deja archivos de >100mb
 queria usar  un formato de compresion pero estaba muy jugado con el tiempo y habia que terminarlo
      
   
## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [VSC] (https://code.visualstudio.com/) - IDE preferido
* [Apache] (https://spark.apache.org/docs/latest/api/python/index.html) - Cuando pandas destruye PC siempre hay una alternativa
* [Databrics](https://community.databricks.com/) cuando tu pc esta al limite siempre llega alguien que nos salva la vida Community Databrics
* [Bello github promocion de proyectos] https://github.com/ para compartir con el mundo mis logros y de mis futuros equipos
* [render] (https://render.com/)   no te tenia fe pero hiciste realidad mis proyectos
* [FastApi](https://fastapi.tiangolo.com/)  que decir  hermosoFRameWork
* [link al video explicativo]](https://www.youtube.com/watch?v=3aHTRn69iNw)
## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

**Marcos Perini** - *Trabajo Inicial-mitad-final y agradecimiento ala comundad Henry!!!* - 

También puedes mirar la lista de todos los [contribuyentes](https://github.com/your/project/contributors) quíenes han participado en este proyecto. ...<----- si diste click sabras darte cuenta que no hay nadie que me ayudo ;-(

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ .. siempre es bienvenido
* Da las gracias públicamente 🤓.
* Siempre son bienvenidas las donaciones MP   pedimelo
* 
* etc.
</div>
