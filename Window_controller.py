from tkinter import *
from gui_control import Gui_Control
from settings_gui_control import Settings_Win_Gui_Control

class Win_Controller:
    def __init__(self):
        #параметры окна
        self.max_winsizeX = 600
        self.max_winsizeY = 800
        
        self.min_winsizeX = 600
        self.min_winsizeY = 800
        
        self.window = Tk()
        #self.window.geometry("1000x1000")
        self.window.minsize(self.min_winsizeX ,self.min_winsizeY)
        self.window.maxsize(self.max_winsizeX,self.max_winsizeY)
        
        
        #кнопка перехода к рулетке
        self.btn_roll_win = Button(text="Додеп")
        self.btn_roll_win.config(padx=20,pady=10,command=self.roll_game_window_render)
        #кнопка настроек
        self.btn_settings_win = Button(padx=20,pady=10,text="Настройки",command=self.settings_window_render)
        #кнопка выхода
        self.btn_exit_win = Button(padx=20,pady=10,text="Выйти",command=self.window.destroy)
        
        #лого
        self.logo_image = PhotoImage(file = 'images/header.gif')
        self.header_logo = Label(image=self.logo_image)
        
        #расположение элементов на лейауте
        
        self.btn_roll_win.grid(padx=20,pady=20,column = 0,row = 2)
        self.btn_exit_win.grid(padx=20,pady=20,column = 0, row = 3,columnspan=2)
        self.btn_settings_win.grid(padx=20,pady=20,column = 1,row = 2)
        self.header_logo.grid(padx=20,pady=20,column = 0, row =0,columnspan=2)
    
    def start_gui(self):
        self.window.mainloop()
    
    def resize_window_to_medium(self):
        self.max_winsizeX = 1000
        self.max_winsizeY = 800 
        self.min_winsizeX = 1000
        self.min_winsizeY = 800
        self.window.minsize(self.min_winsizeX ,self.min_winsizeY)
        self.window.maxsize(self.max_winsizeX,self.max_winsizeY)
        
    def resize_window_to_default(self):
        self.max_winsizeX = 600
        self.max_winsizeY = 800
        self.min_winsizeX = 600
        self.min_winsizeY = 800
        self.window.minsize(self.min_winsizeX ,self.min_winsizeY)
        self.window.maxsize(self.max_winsizeX,self.max_winsizeY)
         
    def return_to_main_window(self):
        self.btn_roll_win.grid()
        self.btn_exit_win.grid()
        self.btn_settings_win.grid()
    
    def roll_game_window_render(self):
        Gui_Control(self)
        self.btn_roll_win.grid_remove()
        self.btn_exit_win.grid_remove()
    
    def settings_window_render(self):
        Settings_Win_Gui_Control(self)
        self.btn_settings_win.grid_remove()
        self.btn_roll_win.grid_remove()
        self.btn_exit_win.grid_remove()