import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, Boolean, LargeBinary
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import join
from sqlalchemy.orm import mapper
from datetime import datetime
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import *
from pprint import pprint

'''
SELECT DISTINCT games_table.game_id,games_table.game_name,genres_table.genre_id,genres_table.genre_name FROM
games_table JOIN games_genres_table ON games_table.game_id = games_genres_table.game_id JOIN
genres_table ON genres_table.genre_id = games_genres_table.genre_id
WHERE genre_name = 'Horror' AND games_table.meta_score>50
'''
'''
найти все игры у которые имеют следующие жанры - action,arcade,shooter
'''

genres_list = ['Artillery',
 '3D',
 'Flight',
 'Gun',
 'Application',
 'Traditional',
 'Horizontal',
 'Static',
 'Golf',
 'Virtual',
 'Tactics',
 'Street',
 'Formula',
 'Basketball',
 'Compilation',
 'City',
 'Cricket',
 'Life',
 'Rail',
 'WWII',
 'Derby',
 'Command',
 'Sim',
 'Futuristic',
 'Metroidvania',
 'Jet',
 '2D',
 'Kart',
 'Visual',
 'Business',
 'Rally',
 'Puzzle',
 'Motorcycle',
 'Submarine',
 'Strategy',
 'Skateboard',
 'Offroad',
 'Football',
 'Turn-Based',
 'One',
 'Pinball',
 'Top-Down',
 'Biking',
 'Skate',
 'Action',
 'Light',
 'Shooter',
 'Rhythm',
 'Truck',
 'Text',
 'Spaceship',
 'Sci-Fi',
 'PC-style',
 'Trivia',
 'Large',
 'Motocross',
 'Open-World',
 'Movie',
 'Linear',
 'Skateboarding',
 'Driving',
 'Individual',
 'Ship',
 "Shoot-'Em-Up",
 'Demolition',
 'Management',
 'Vertical',
 'Mission-based',
 'Career',
 'Civilian',
 'Battle',
 'Roguelike',
 'Athletics',
 'Scrolling',
 'Survival',
 'Miscellaneous',
 'Role-Playing',
 'Arcade',
 'Car',
 'Rugby',
 'Music',
 'WWI',
 'Hockey',
 'MOBA',
 'RPG',
 'Boxing',
 'Ski',
 'Show',
 'Console-style',
 'Vehicle',
 'Combat',
 'Tank',
 'Multiplayer',
 'Soccer',
 'Minigame',
 'Platformer',
 'Tactical',
 'General',
 'Marine',
 'Modern',
 'Olympic',
 'Government',
 'First-Person',
 'Horror',
 'Adventure',
 'Fantasy',
 'Space',
 'Fighting',
 'Bowling',
 'Snowboarding',
 'Surf',
 'Snowboard',
 'Third-Person',
 'Old',
 'Board',
 'Wakeboard',
 'Massively',
 'Tycoon',
 'Real-Time',
 'Plane',
 'Military',
 'Parlor',
 'Alternative',
 'Automobile',
 'Sub',
 'Tennis',
 'Baseball',
 'Arts',
 'Matching',
 'Defense',
 'Interactive',
 'Gambling',
 'Billiards',
 'Sandbox',
 'Logic',
 'Online',
 'Team',
 'Edutainment',
 'Breeding/Constructing',
 'Mech',
 'Point-and-Click',
 'Building',
 'Martial',
 'Racing',
 'Train',
 'Party',
 'Ice',
 'Japanese-Style',
 'Games',
 'Simulation',
 'Wargame',
 'Other',
 'Western-Style',
 'Game',
 'Surfing',
 'Historic',
 'Novel',
 'Helicopter',
 'Stock',
 'Card',
 'Small',
 'Sports']

engine = create_engine('sqlite:///games_data.db')  
metadata = MetaData(engine)

DBSession = sessionmaker(bind = engine)

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

"""
def get_all_genres_list():
    genres_list=[]
    with open("ALL_UNIQUE_GENRES.csv","r") as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                genres_list.append(row["genre_name"])
            pprint(genres_list)
"""
def get_games_of_date_period(date_range,metascore_range,genres_str_list):
    session = DBSession()
    dict_of_games={}
    date_from = f"{date_range[0]}-01-01"
    date_to = f"{date_range[1]}-12-31"
    metascore_from = metascore_range[0]
    metascore_to = metascore_range[1]
    
    result = None
    print(genres_str_list)
    if not genres_str_list or genres_str_list[0]=="None":
        result = session.query(Games_Table,Genres_Table).join(Games_Genres_Table,Games_Table.game_id == Games_Genres_Table.game_id)\
        .join(Genres_Table,Genres_Table.genre_id == Games_Genres_Table.genre_id).filter(Games_Table.release_date>date_from,Games_Table.release_date<date_to,
        Games_Table.meta_score>metascore_from,Games_Table.meta_score<metascore_to)
    else:
        template="genre_name='{}' OR "
        where_statement=(template*len(genres_str_list)).format(*genres_str_list).strip("OR ")
        #print("this is where statement",print(genres))
        #input(where_statement)
        result = session.query(Games_Table,Genres_Table).join(Games_Genres_Table,Games_Table.game_id == Games_Genres_Table.game_id)\
        .join(Genres_Table,Genres_Table.genre_id == Games_Genres_Table.genre_id).filter(Games_Table.release_date>date_from,Games_Table.release_date<date_to,
        Games_Table.meta_score>metascore_from,Games_Table.meta_score<metascore_to).filter(text(where_statement))
    
    for c in result:
        #print(c[0].game_name,c[1].genre_name)
        dict_of_games[c[0].game_name] = c[0].rarity
    #print(dict_of_games)
    return dict_of_games
    
    
#get_games_of_date_period()
#get_all_genres_list()
