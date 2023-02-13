from tkinter import *
from tkinter import messagebox
from data_manager import Data_Manager

def dummy_method():
    print("hello")

class Wheel_Win_Control:
    def __init__(self,canvas_container,x_place,y_place):
        #настройки
        self.x_pos=x_place
        self.y_pos=y_place

        self.d_manager = Data_Manager()    
        #подцепляет настройки скорости
        self.speed_params_dict = self.d_manager.get_dict_of_speed_params()
        #подцепляет настройки жанров
        self.genres_category_dict = self.d_manager.get_all_genres_option()
        self.raw_current_genre_preset=self.d_manager.get_current_genre_preset()
        self.current_genre_preset =" ".join(self.d_manager.get_current_genre_preset().split("_"))
        
        #подцепляет настройки диапазонов
        self.years_range_list=self.d_manager.get_list_of_year_range_params()
        self.metascore_range_list=self.d_manager.get_list_of_metascore_range_params()
        
        #окно-контейнер
        self.window=canvas_container
        
        #параметры элементов
        self.roulette_cnv_size = 650
        self.roulette_cnv_height = 520
     
        #канвас
        self.wheel_settings_cnv = Canvas(width = self.roulette_cnv_size,height = self.roulette_cnv_height,bg="#dfdfde")
        
        #спинбоксы скорости рулетки и времени раскрутки
        self.cont_obj_speed= IntVar()
        self.cont_obj_speed.set(self.speed_params_dict["velocity"])
        self.speed_spinbox = Spinbox(width=9,from_=0,to=25,increment=1,textvariable = self.cont_obj_speed,state="readonly")  
        self.wheel_settings_cnv.create_window(150,60,anchor=NW,window=self.speed_spinbox)
        
        self.cont_obj_time = IntVar()
        self.cont_obj_time.set(self.speed_params_dict["roll_time"])
        self.time_spinbox = Spinbox(width=9,from_=0,to=15,increment=1,textvariable = self.cont_obj_time,state="readonly")  
        self.wheel_settings_cnv.create_window(150,100,anchor=NW,window=self.time_spinbox)
        
        #текст для скорости рулетки
        self.speed_spbx_txt = self.wheel_settings_cnv.create_text((75,70), text="Скорость рулетки")
        self.time_spbx_txt = self.wheel_settings_cnv.create_text((75,110), text="Время раскрутки (сек)")
        self.validation_txt = self.wheel_settings_cnv.create_text((360,420),text="",state="hidden")
        
        #скейлы для даты релиза
        self.year_scale_from = Scale(from_=1998,to_=2016,length = 100,orient="horizontal",command=self.control_todate_scale) 
        self.year_scale_from.set(self.years_range_list[0])
        self.year_scale_to = Scale(from_=1998,to_=2016,length = 100,orient="horizontal",command=self.control_fromdate_scale)
        self.year_scale_to.set(self.years_range_list[1])
        self.wheel_settings_cnv.create_window(310,180,anchor=NW,window=self.year_scale_from)
        self.wheel_settings_cnv.create_window(310,220,anchor=NW,window=self.year_scale_to)
        
        #текст для даты релиза
        self.metascore_spbx_txt = self.wheel_settings_cnv.create_text((355,160), text="Дата релиза игр пула")
        self.metascoreFrom_spbx_txt = self.wheel_settings_cnv.create_text((290,195), text="От: ")
        self.metascoreTo_spbx_txt = self.wheel_settings_cnv.create_text((290,240), text="До:") 
        
        #скейлы для диапазона метаскора
        self.metascore_scale_from = Scale(from_=0,to_=100,length = 100,orient="horizontal",command=self.control_toMscore_scale)
        self.metascore_scale_from.set(self.metascore_range_list[0])
        self.metascore_scale_to = Scale(from_=0,to_=100,length = 100,orient="horizontal",command=self.control_fromMscore_scale)
        self.metascore_scale_to.set(self.metascore_range_list[1])
        self.wheel_settings_cnv.create_window(310,50,anchor=NW,window=self.metascore_scale_from)
        self.wheel_settings_cnv.create_window(310,90,anchor=NW,window=self.metascore_scale_to)
        
        #текст для диапазона метаскора 
        self.dateRelease_spbx_txt = self.wheel_settings_cnv.create_text((340,30), text="Диапазон оценок игр пула")
        self.dateFrom_spbx_txt = self.wheel_settings_cnv.create_text((290,70), text="От: ")
        self.dateTo_spbx_txt = self.wheel_settings_cnv.create_text((290,110), text="До:")  

        
        #выпадающий список с группами по жанрам
        options=list(self.genres_category_dict.values())
        self.cont_obj_str= StringVar()
        self.cont_obj_str.set(self.current_genre_preset)
        self.group_of_genres=OptionMenu(self.wheel_settings_cnv,self.cont_obj_str,*options)
        self.wheel_settings_cnv.create_window(470,75,anchor=NW,window=self.group_of_genres)
        
        #текст для списка игр по жанрам
        self.list_spbx_txt = self.wheel_settings_cnv.create_text((530,50), text="Список пресетов по\n группам жанров:")
        
        #кнопка сохранения
        self.save_speed_btn = Button(text="Сохранить",padx=5,pady=10,command=self.save_speed_settings)
        self.wheel_settings_cnv.create_window(325,450,anchor=NW,window=self.save_speed_btn)
        

        

        

        
        #помещение элемента окна в контейнер
        self.window.create_window((self.x_pos,self.y_pos),anchor=NW,window=self.wheel_settings_cnv)
        
   
    def control_fromdate_scale(self,value):
        if int(int(self.year_scale_to.get())-int(self.year_scale_from.get()))<0:
            self.year_scale_from.set(str(int(self.year_scale_from.get())-1))
    
    def control_todate_scale(self,value):
        if int(int(self.year_scale_from.get())-int(self.year_scale_to.get()))>0:
            self.year_scale_to.set(str(int(self.year_scale_to.get())+1))
        
    def control_fromMscore_scale(self,value):
        if int(int(self.metascore_scale_to.get())-int(self.metascore_scale_from.get()))<0:
            self.metascore_scale_from.set(str(int(self.metascore_scale_from.get())-1))
        
    def control_toMscore_scale(self,value):
        if int(int(self.metascore_scale_from.get())-int(self.metascore_scale_to.get()))>0:
            self.metascore_scale_to.set(str(int(self.metascore_scale_to.get())+1))
    
    def save_speed_settings(self):
        self.wheel_settings_cnv.itemconfigure(self.validation_txt,text="Настройки скорости рулетки \nи отрезков удачно сохранены!",fill="#248e13",state="normal")    
        
        #сохранение диапазонов
        date_from = str(self.year_scale_from.get())
        date_to = str(self.year_scale_to.get())
        metascore_from = str(self.metascore_scale_from.get())
        metascore_to = str(self.metascore_scale_to.get())
        self.d_manager.write_year_range_settings({"from":date_from,"to":date_to})
        self.d_manager.write_metascore_range_settings({"from":metascore_from,"to":metascore_to})
        
        #параметры скорости 
        speed = self.speed_spinbox.get()
        time = self.time_spinbox.get()
        self.d_manager.write_speed_settings({"velocity":speed,"roll_time":time})
        
        #сохранение текущего пресета
        game_preset = self.cont_obj_str.get()
        game_preset="_".join(game_preset.split())
        self.d_manager.write_preset_settings(game_preset)
        
        