# sgp_utils
Librería para trabajar más cómodamente en python y postgis.

## Funciones ##
* to_spatialite (gdf, tb, ruta, srid, geomtype, some_id):
~~~
Guarda un geodataframe a spatialite

argumentos:
gdf= geodataframe
tb = nombre de la tabla
ruta = ruta de guardado
srid = es el sistema de referencia
geomtype = tipo de geometría
some_id = identificador único
~~~
    
* do(sql, connection):
~~~
Tarea que ejecuta un sql en postgres

argumentos:
sql= como string de la sql a realizar
connection= definición de la conexión (a definir previamente por el usuario)
~~~

* do_sql(sql, tb, some_id, connection):
~~~
Tarea que ejecuta un sql en postgres (crea tabla + clave primaria )

argumentos:
sql= como string de la sql a realizar
tb= nombre de la tabla a crear
some_id = clave id primaria
connection= definición de la conexión (a definir previamente por el usuario)
~~~
    
* do_spatial(sql, tb, some_id, connection):
~~~
Tarea que ejecuta un sql en postgres (crea tabla + clave primaria + índice espacial)

argumentos: 
sql= como string de la sql a realizar
tb= nombre de la tabla a crear
some_id = clave id primaria
connection= definición de la conexión (a definir previamente por el usuario)
~~~
    
* to_multi (gdf):
~~~
Tarea que comprueba si la geometría de un geodataframe es multiparte, y si no lo fuera, la convierte en multiparte

argumentos:
gdf = geodataframe sobre el que trabajar
~~~
    
## Requerimientos de instalación: ##
Esta librería depende de: os, sqlite3, pandas, geopandas, sqlalchemy, psycopg2, time
