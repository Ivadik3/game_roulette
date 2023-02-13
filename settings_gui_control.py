from tkinter import *
from chances_settings import Chance_Win_Control
from wheel_settings import Wheel_Win_Control

class Settings_Win_Gui_Control:
    def __init__(self,main_window):
       
        
        #объект осовного окна, чтобы выходить обратно на мейн окно
        self.Window_Controller = main_window
        self.Window_Controller.resize_window_to_medium()
        self.window = self.Window_Controller.window
         
        #параметры элементов
        self.cnv_width = self.Window_Controller.min_winsizeX 
        self.cnv_height = self.Window_Controller.min_winsizeY+100
        self.first_cnv_block = Canvas(width = self.cnv_width-20 ,height = (self.cnv_height/2)+100,bg="#dfdfde")
        
        #кнопка назад
        self.go_back_btn = Button(text="Назад",command=self.get_back_to_main_window,padx=10,pady=5)
        
        #добавление окон настроек
        self.chances_cnv = Chance_Win_Control(self.first_cnv_block,20,20)
        self.wheel_settings_cnv = Wheel_Win_Control(self.first_cnv_block,310,20)
        
        
        #расположение элементов 
        self.go_back_btn.grid(column=0,row = 4,columnspan=2,padx=2,pady=2)
        self.first_cnv_block.grid(padx=5,pady=5,column = 0, row = 1)
        
    #возвратится назад на main_window 
    def get_back_to_main_window(self):
        self.Window_Controller.resize_window_to_default()
        self.first_cnv_block.grid_remove()
        self.go_back_btn.grid_remove()
        self.Window_Controller.return_to_main_window()