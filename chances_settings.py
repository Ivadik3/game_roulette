from tkinter import *
from tkinter import messagebox
from data_manager import Data_Manager

class Chance_Win_Control:
    def __init__(self,canvas_container,x_place,y_place):
        #параметры элементов
        self.roulette_cnv_size = 250
        self.roulette_cnv_height = 350
        self.x_pos=x_place
        self.y_pos=y_place
        
        #инициализация служебных классов
        self.window = canvas_container
        self.d_manager = Data_Manager()
        self.chances_offset = self.d_manager.get_dict_of_chances()
        #переменные
        self.start_percent_sum=(self.chances_offset["common"]+self.chances_offset["rare"]+self.chances_offset["mythical"]+self.chances_offset["legendary"]+self.chances_offset["t2t"])
        self.result_even=0
        
        #канвас и объекты окна настройки рандома
        self.chances_cnv = Canvas(width = self.roulette_cnv_size,height = self.roulette_cnv_height,bg="#dfdfde")
        #спинбоксы
        self.cont_obj_common_spbx = DoubleVar()
        self.cont_obj_common_spbx.set(self.chances_offset["common"])
        self.common_spinbox = Spinbox(width=9,from_=0,to=1,increment=0.01,textvariable = self.cont_obj_common_spbx,state="readonly",command=self.changing_percent)  
        self.chances_cnv.create_window(self.roulette_cnv_size/2,10,anchor=NW,window=self.common_spinbox)
        
        self.cont_obj_rare_spbx = DoubleVar()
        self.cont_obj_rare_spbx.set(self.chances_offset["rare"])
        self.rare_spinbox = Spinbox(width=9,from_=0,to=1,increment=0.01,textvariable = self.cont_obj_rare_spbx,state="readonly",command=self.changing_percent)
        self.chances_cnv.create_window(self.roulette_cnv_size/2,50,anchor=NW,window=self.rare_spinbox)
        
        self.cont_obj_mythical_spbx = DoubleVar()
        self.cont_obj_mythical_spbx.set(self.chances_offset["mythical"])
        self.mythical_spinbox = Spinbox(width=9,from_=0,to=1,increment=0.01,textvariable = self.cont_obj_mythical_spbx,state="readonly",command=self.changing_percent)
        self.chances_cnv.create_window(self.roulette_cnv_size/2,90,anchor=NW,window=self.mythical_spinbox)
        
        self.cont_obj_legendary_spbx = DoubleVar()
        self.cont_obj_legendary_spbx.set(self.chances_offset["legendary"])
        self.legendary_spinbox = Spinbox(width=9,from_=0,to=1,increment=0.01,textvariable = self.cont_obj_legendary_spbx,state="readonly",command=self.changing_percent)
        self.chances_cnv.create_window(self.roulette_cnv_size/2,130,anchor=NW,window=self.legendary_spinbox)
        
        self.cont_obj_t2t_spbx = DoubleVar()
        self.cont_obj_t2t_spbx.set(self.chances_offset["t2t"])
        self.t2t_spinbox = Spinbox(width=9,from_=0,to=1,increment=0.01,textvariable = self.cont_obj_t2t_spbx,state="readonly",command=self.changing_percent)
        self.chances_cnv.create_window(self.roulette_cnv_size/2,170,anchor=NW,window=self.t2t_spinbox)
        
        #надписи напротив спинбоксов
        self.common_spbx_txt = self.chances_cnv.create_text((self.roulette_cnv_size/3,20), text="common")
        self.rare_spbx_txt = self.chances_cnv.create_text((self.roulette_cnv_size/3,60), text="rare")
        self.mythical_spbx_txt = self.chances_cnv.create_text((self.roulette_cnv_size/3,100), text="mythical")
        self.legendary_spbx_txt = self.chances_cnv.create_text((self.roulette_cnv_size/3,140), text="legendary")
        self.t2t_spbx_label_txt = self.chances_cnv.create_text((self.roulette_cnv_size/3,180), text="t2t")
        
        #надписи о нераспределенных процентах        
        self.percent_sum_txt = self.chances_cnv.create_text((self.roulette_cnv_size/2,230), text="Сумма вероятностей равна 1. \n (все ок)")
        #надпись о удачном/неудачном сохранении данных процентов
        self.validation_txt = self.chances_cnv.create_text((self.roulette_cnv_size/2,280),text="",state="hidden")
        
        #self.percent_sum_info_txt = self.chances_cnv.create_text((self.roulette_cnv_size/3,230), text="Процентов нераспределено:")
        
        #кнопка сохранения процентных вероятностей
        self.save_percentage_btn = Button(text="Сохранить",command=self.save_percentage_settings)
        self.chances_cnv.create_window((self.roulette_cnv_size/2)-20,310,anchor=NW,window=self.save_percentage_btn)
        
        #помещение всех элементов на грид лейаут
        self.window.create_window((self.x_pos,self.y_pos),anchor=NW,window=self.chances_cnv)

        
    def changing_percent(self):
        spinbox_sum = float(self.common_spinbox.get())+float(self.rare_spinbox.get())+float(self.mythical_spinbox.get())+float(self.legendary_spinbox.get())+float(self.t2t_spinbox.get())
        self.result_even=self.start_percent_sum-spinbox_sum
        if self.result_even<0:
            self.chances_cnv.itemconfigure(self.percent_sum_txt,text=f"Необходимо убрать процентов: {round(self.result_even*100*-1,2)}")
        elif self.result_even>0:
            self.chances_cnv.itemconfigure(self.percent_sum_txt,text=f"Необходимо добавить процентов: {round(self.result_even*100,2)}")
        else:
            self.chances_cnv.itemconfigure(self.percent_sum_txt,text="Сумма вероятностей равна 1.")
        
        #print(result_even)
        pass
    
    
    #возвратится назад на main_window 
    def get_back_to_main_window(self):
        pass
        
    def save_percentage_settings(self):
        if self.result_even!=0:
            self.chances_cnv.itemconfigure(self.validation_txt,text="Сумма вероятностей не равна нулю, \n настройки не сохранены!",fill="#cb3326",state="normal")
        else:
            dict_to_write={
                "common":self.common_spinbox.get(),
                "rare":self.rare_spinbox.get(),
                "mythical":self.mythical_spinbox.get(),
                "legendary":self.legendary_spinbox.get(),
                "t2t":self.t2t_spinbox.get()
            }
            self.d_manager.write_chances_settings(dict_to_write)
            self.chances_cnv.itemconfigure(self.validation_txt,text="Настройки вероятностей \n удачно сохранены!",fill="#248e13",state="normal")