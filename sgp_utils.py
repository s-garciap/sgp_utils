#!/usr/bin/env python
# coding: utf-8


import os
import sqlite3
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import psycopg2
import time

__version__ = '0.1'

def internal_task (gdf, tb, ruta, srid, geomtype, some_id):
    ##quita la gemetría del geodataframe
    df = gdf.drop(['geometry'], axis=1)
    
    ##para guardarlo en sqlite sin geometria
    con = sqlite3.connect (ruta)
    df.to_sql(tb, con = con, if_exists='replace', index=False)
    
    ##ahora generamos una nueva columna que se llama geometría
    with sqlite3.connect(ruta) as conn:
        conn.enable_load_extension(True)
        conn.load_extension("mod_spatialite")
        conn.execute("SELECT InitSpatialMetaData(1);")
        conn.execute(
            f'''
            SELECT AddGeometryColumn('{tb}', 'geometry', {srid}, '{geomtype}', 2);
            '''
        )
    
    ##pasamos la geometría de geopandas a spatialite
    import shapely.wkb as swkb
    records = [
        {f'{some_id}': gdf[some_id].iloc[i], 'wkb': swkb.dumps(gdf.geometry.iloc[i])}
        for i in range(gdf.shape[0])
    ]
    ##generamos un tuple
    tuples = tuple((d['wkb'], d[f'{some_id}']) for d in records)
    ##incorporamos los tuples de geometria en la tabla
    with sqlite3.connect(ruta) as conn:
        conn.enable_load_extension(True)
        conn.load_extension("mod_spatialite")
        conn.executemany(
            f'''
            UPDATE {tb}
            SET geometry=GeomFromWKB(?, {srid})
            WHERE {tb}.{some_id} = ?
            ''', (tuples)
        )
    ## hacemos un índice espacial
    with sqlite3.connect(ruta) as conn:
        conn.enable_load_extension(True)
        conn.load_extension("mod_spatialite")
        conn.execute("SELECT InitSpatialMetaData(1);")
        conn.execute(
            f'''
            SELECT CreateSpatialIndex('{tb}', 'geometry');
            '''
    )
    print(f'Spatialite "{tb}" succesful created in "{ruta}"!')


def to_spatialite (gdf, tb, ruta, srid, geomtype, some_id):
    '''
    guarda un geodataframe a spatialite
    
    requiere:
    gdf= geodataframe
    tb = nombre de la tabla
    ruta = ruta de guardado
    srid = es el sistema de referencia
    geomtype = tipo de geometría
    some_id = identificador único
    '''
    
    ##para hacernos la vida más facil, imprimimos tipo de geometria unica
    print(gdf.geom_type.unique())
    
    ##define el nombre y ruta
    if ruta == '':
        ruta = tb + '.sqlite'
    else:
        ruta = ruta + '/' + tb + '.sqlite'
        
    ## chequea si el archivo existe y pregunta si debe reemplazarlo
    if os.path.exists(ruta):
        print('The file exists')
        while True:
            decision = input(''' 
    - Enter A to remove and create one new
    - Enter B to stop
    ''')
            if decision == 'A':
                os.remove(ruta)
                print('The file was removed to create a new one')
                internal_task (gdf, tb, ruta, srid, geomtype, some_id)
                break
            elif decision == 'B':
                print('Process interrupted by user request')
                break
            else:
                print('you have made an invalid choice (A or B), try again!')
    else:
        print('The file does not exist')
        internal_task (gdf, tb, ruta, srid, geomtype, some_id)


def do(sql, connection):
    '''
    tarea que ejecuta un sql en postgres
    requiere: sql= como string de la sql a realizar
    connection= definición de la conexión (a definir previamente por el usuario)
    '''
    ##connection = "user={username} dbname={dbname} password={password} host={host} port={port}".format(**conf)
    con = psycopg2.connect(connection)
    cursor = con.cursor()
  
    sql = sql 
    
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()
    return

def do_sql(sql, tb, some_id, connection):
    '''
    tarea que ejecuta un sql en postgres (crea tabla + clave primaria )
    requiere: sql= como string de la sql a realizar
    tb= nombre de la tabla a crear
    some_id = clave id primaria
    connection= definición de la conexión (a definir previamente por el usuario)
    '''
    ##connection = "user={username} dbname={dbname} password={password} host={host} port={port}".format(**conf)
    con = psycopg2.connect(connection)
    cursor = con.cursor()
    
    pre = f'''drop table if exists {tb};
            create table {tb} as'''
    
    post = f'''
            ALTER TABLE {tb}
            ADD PRIMARY KEY ({some_id});'''
    
    sql = pre + sql + '; ' +  post
    
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()
    return

def do_spatial(sql, tb, some_id, connection):
    '''
    tarea que ejecuta un sql en postgres (crea tabla + clave primaria + índice espacial)
    requiere: sql= como string de la sql a realizar
    tb= nombre de la tabla a crear
    some_id = clave id primaria
    connection= definición de la conexión (a definir previamente por el usuario)
    '''
    ##connection = "user={username} dbname={dbname} password={password} host={host} port={port}".format(**conf)
    con = psycopg2.connect(connection)
    cursor = con.cursor()
    
    pre = f'''drop table if exists {tb};
           create table {tb} as'''
    
    post = f'''
            ALTER TABLE {tb}
           ADD PRIMARY KEY ({some_id});
           
           CREATE INDEX {tb}_geometry_idx
           ON {tb}
           USING GIST (geometry);
           '''
    
    sql = pre + sql + '; ' +  post
    
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()
    return



def to_multi (gdf):
    print('The geometry type is: ' + gdf.geom_type.unique())
    if gdf.geom_type.unique().any() == 'LineString' or gdf.geom_type.unique().any() == 'MultiLineString':
        from shapely.geometry.linestring import LineString
        from shapely.geometry.multilinestring import MultiLineString

        gdf["geometry"] = [MultiLineString([feature]) if isinstance(feature, LineString)             else feature for feature in gdf["geometry"]]
        return gdf
    
    elif gdf.geom_type.unique().any() == 'Polygon' or gdf.geom_type.unique().any() == 'MultiPolygon':
        from shapely.geometry.polygon import Polygon
        from shapely.geometry.multipolygon import MultiPolygon

        gdf["geometry"] = [MultiPolygon([feature]) if isinstance(feature, Polygon)             else feature for feature in gdf["geometry"]]
        return gdf
    
    elif gdf.geom_type.unique().any() == 'Point' or gdf.geom_type.unique().any() == 'MultiPoint':
        from shapely.geometry.point import Point
        from shapely.geometry.multipoint import MultiPoint

        gdf["geometry"] = [MultiPoint([feature]) if isinstance(feature, Point)             else feature for feature in gdf["geometry"]]
        return gdf
    
    else:
        return gdf

