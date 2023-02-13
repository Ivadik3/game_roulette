from numpy.random import choice
import configparser
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, Boolean
from datetime import datetime
from table_initialize import Games_Table,Genres_Table,Games_Genres_Table
import table_initialize

class Data_Manager:
    
    def __init__(self):
        
        
        """
        self.games_dict={
            "prototype НА ХАРДЕ":"common",
            "5 ФК ПОДРЯД В osu!":"common",
            "КАТКА В counter-strike":"common",
            "persona 5":"rare",
            "dark-ЗАСАСИ":"rare",
            "dark-souls 1":"rare",
            "vice-city на саб 50":"rare",
            "dark-souls 2":"mythical",            
            "dead-space":"mythical",
            "system-shock 2":"mythical",
            "gunpoint":"legendary",
            "T2T":"t2t",
            "T2T-PSP":"t2t",
        }
        """
        #test_list = self.get_list_of_genres("пострелять_под_пиво")
        #print(test_list,"this is genres list")
        
        #print(test_dict)
        #test_dict = self.get_all_genres_option()
        
        #test_list=self.get_genres_by_current_preset()
        #print(test_list)
        
        self.date_range=self.get_list_of_year_range_params()
        self.metascore_range=self.get_list_of_metascore_range_params()
        print(self.date_range,self.metascore_range)
        self.games_dict=None
        self.drop_chances = self.get_dict_of_chances()
    
    def init_new_game_pool(self):
        current_preset=self.get_genres_by_current_preset()
        self.games_dict = table_initialize.get_games_of_date_period(self.date_range,self.metascore_range,current_preset)
        print(len(self.games_dict))
        valid_chanes = set([rarity for game,rarity in self.games_dict.items()])
        self.current_game_chances = {}
        for i in valid_chanes:
            if i in self.drop_chances:
                self.current_game_chances[i] = self.drop_chances[i]
        print(len(self.current_game_chances),len(self.drop_chances))
        if len(self.current_game_chances)!=len(self.drop_chances):
            value_to_add=1
            for key,value in self.current_game_chances.items():
                value_to_add-=value
            print(value_to_add)
            value_to_add = value_to_add/len(self.current_game_chances)
            for key,value in self.current_game_chances.items():
                self.current_game_chances[key]+=value_to_add
            print(self.current_game_chances)
        print(self.current_game_chances)
        
    def pick_random_game(self):
        """
        метод для формирования одной ячейки во время ролла
        """
        print(list(self.drop_chances.keys()))
        print(sum(list(self.drop_chances.values())))
        rarity_choice = choice(list(self.current_game_chances.keys()),1,replace=False,p=list(self.current_game_chances.values()))
        print(len(self.games_dict))
        print(rarity_choice,"this is rarity choice")
        games_by_rarity=[game_name for game_name,rarity in self.games_dict.items() if rarity==rarity_choice[0]]
        #print(games_by_rarity)
        game_choice = choice(games_by_rarity,1)
        print(game_choice,"this is game choice")
        return {"game_name":game_choice[0],"game_rarity":rarity_choice[0]}
    
    
    def get_genres_by_current_preset(self):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        current_preset_block = config["CURRENT_GENRE_PRESET"]
        current_preset=None
        for line in current_preset_block:
            current_preset=current_preset_block.get(line)
        
        genres_block=config["GAMES_GENRES_TYPE"]
        genres_list=None
        for line in genres_block:
            if line == current_preset:
                genres_list=genres_block.get(line)
                genres_list=genres_list.split(",")
        return genres_list   
    
    def get_all_genres_option(self):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        genres_block = config["GAMES_GENRES_TYPE"]
        genres_dict={}
        for line in genres_block:
            print(line)
            genres_dict[line]=" ".join(line.split("_"))
        return genres_dict
    
    def get_current_genre_preset(self):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        genres_block = config["CURRENT_GENRE_PRESET"]
        current_preset=""
        for line in genres_block:
            current_preset=genres_block.get(line)
        return current_preset
    
    def get_dict_of_chances(self):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        chances_block = config["ROULETTE_CHANCES_PARAMS"]
        chances_dict = {}
        for line in chances_block:
            chances_dict[line] = chances_block.getfloat(line)   
        return chances_dict
        
    def get_dict_of_speed_params(self):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        chances_block = config["ROULETTE_SPEED_PARAMS"]
        chances_dict = {}
        for line in chances_block:
            chances_dict[line] = chances_block.getfloat(line)   
        return chances_dict
    
    def get_list_of_year_range_params(self):
        pass
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        years_block = config["ROULETTE_YEAR_RANGE"]
        year_list = []
        for line in years_block:
            year_list.append(years_block.getint(line))
        return year_list
        
    def get_list_of_metascore_range_params(self):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        score_block = config["METASCORE_RANGE"]
        score_list = []
        for line in score_block:
            score_list.append(score_block.getint(line))
        return score_list
    
    def write_speed_settings(self,val_dict):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        for key,value in val_dict.items():
            config.set("ROULETTE_SPEED_PARAMS",key,value)
        with open("config.ini","w",encoding="utf-8") as configfile:
            config.write(configfile)
    
    def write_chances_settings(self,val_dict):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        for key,value in val_dict.items():
            config.set("ROULETTE_CHANCES_PARAMS",key,value)
        with open("config.ini","w",encoding="utf-8") as configfile:
            config.write(configfile)

    def write_year_range_settings(self,val_dict):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        for key,value in val_dict.items():
            config.set("ROULETTE_YEAR_RANGE",key,value)
        with open("config.ini","w",encoding="utf-8") as configfile:
            config.write(configfile)
        
    def write_metascore_range_settings(self,val_dict):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        for key,value in val_dict.items():
            config.set("METASCORE_RANGE",key,value)
        with open("config.ini","w",encoding="utf-8") as configfile:
            config.write(configfile)

    def write_preset_settings(self,variable):
        config = configparser.ConfigParser()
        config.read("config.ini",encoding="utf-8")
        config.set("CURRENT_GENRE_PRESET","current_preset",variable)
        with open("config.ini","w",encoding="utf-8") as configfile:
            config.write(configfile)