import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, Boolean, LargeBinary
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.orm import mapper
from datetime import datetime
import csv


def getting_records(engine,table):
    conn = engine.connect()
    select_query = select(table)
    result = conn.execute(select_query)
    for row in result:
        print(row)


engine = create_engine('sqlite:///games_data.db')
        
#connection = engine.connect()
metadata = MetaData(engine)

"""      
games = Table('games_table', metadata,
    Column('id',Integer(),primary_key=True),
    Column('game_id', Integer(),unique=True),
    Column('game_name', String(200), nullable=False),
    Column('release_date', DateTime()),    
    Column('meta_score',Integer()),
    Column('rarity', String(200), default = "common"),    
    Column('was_picked',Boolean(),default = False)
        )

genres = Table('genres_table', metadata,
    Column('genre_id', Integer(), primary_key=True),
    Column('genre_name', String(200), nullable=False)
        )
        
relative = Table('games_genres_table', metadata,
    Column('id', Integer(), primary_key=True),
    Column('game_id', ForeignKey("games_table.game_id")),
    Column('genre_id', ForeignKey("genres_table.genre_id")),
        )
"""

games = Table('games_table',metadata,autoload=True)
genres = Table('genres_table',metadata,autoload=True)
relative = Table('games_genres_table',metadata,autoload=True)

class Games_Table(object):
    pass

class Genres_Table(object):
    pass
    
class Games_Genres_Table(object):
    pass
     
mapper(Games_Table,games)
mapper(Genres_Table,genres)
mapper(Games_Genres_Table,relative)

getting_records(engine,genres)

input("done")
        
"""
metadata.create_all(engine)

list_of_dicts=[]

with open("game_genre_relative.csv","r") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        list_of_dicts.append(
            {
            "game_id":row["game_id"],
            "genre_id":row["genre_id"]
            }
        )
operation = connection.execute(insert(relative),list_of_dicts) 
input("done")
"""

"""
list_of_dicts=[]

with open("ALL_UNIQUE_GENRES.csv","r") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        list_of_dicts.append(
            {
            "genre_id":row["genre_id"],
            "genre_name":row["genre_name"]
            }
        )
operation = connection.execute(insert(genres),list_of_dicts) 
input("done")
"""


"""
#adding enries in games_table 
list_of_dicts=[]
year_range=range(1998,2017)
iter_val=0

for i in year_range:
    with open(f'PC_{i}.csv','r') as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            #crafting date entry
            print(row["game_name"])
            date_release = list(map(int,row['release_date'].split()))
            date_release = datetime(date_release[0],date_release[1],date_release[2])
            #metascore to int 
            metascore = int(row["meta_score"])
            
            list_of_dicts.append(
                {
                "game_id":iter_val,
                "game_name":row["game_name"],
                "release_date":date_release,
                "meta_score": metascore
                }
            )
            iter_val+=1
            #insert_query = insert(games).values(
            #    game_name = row['game_name'],
            #    release_date = date_release,
            #    meta_score = metascore)
                
operation = connection.execute(insert(games),list_of_dicts) 
input("done")



"""