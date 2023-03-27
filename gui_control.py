from tkinter import *
from game_cell import Game_cell
import time
from game_control import Game_Control
from data_manager import Data_Manager

class Gui_Control:
    #BACKGROUND_COLOR = "#B1DDC6"
    def __init__(self,main_window):
        
        
        #параметры размеров окон программы
        self.winsize = 800
        self.roulette_cnv_size = 400
        #параметры цвета ячеек
        '''
        Можно вынести в config.ini
        '''
        self.cell_colors={
            "common":"#8a908a",
            "rare":"#346bcd",
            "mythical":"#9b14e8", 
            "legendary":"#fff414",
            "t2t":"#84462c",
        }
        
        #инициализация служебных классов из модулей и объектов не граф интерфейса
        self.gm_cont = Game_Control(self.roulette_cnv_size,self.roulette_cnv_size)
        self.d_manager = Data_Manager()
        self.d_manager.init_new_game_pool()
        self.speed_and_velo_params = self.d_manager.get_dict_of_speed_params()
     
        #параметры рулетки
        self.start_velocity=self.speed_and_velo_params["velocity"]
        self.rolling_time=self.speed_and_velo_params["roll_time"]
        self.time_gap_to_reduce=1
        self.reduce_vel_param = self.start_velocity/self.rolling_time
        
        #инициализация необходимых ткинтеровских элементов для программы     
        #инициализация основого окна и основного canvas
        self.Window_Controller = main_window #объект главного окна был передан в эту переменную, это нужно чтобы вернуться на мейн окно позже
        self.window = self.Window_Controller.window
        #канвас рулетки
        self.cnv_roulette=Canvas(width = self.roulette_cnv_size,height = self.roulette_cnv_size,bg="#000000") 


        #инициализация доп элементов
        
       
        
        #канвас для выпавшей игры, в нем содержится картинка и rectangle
        self.result_canvas = Canvas(width=400,height=80)
        self.unknown_game_image = PhotoImage(file = 'images/unknown_game.gif')
        self.unknown_game_label = self.result_canvas.create_image(0, 0, image = self.unknown_game_image, anchor = NW)
        self.rec_rolled_game = self.result_canvas.create_rectangle(0,0,400,80,fill="#FFFFFF",outline="#FFFFFF")
        self.text_rolled_game = self.result_canvas.create_text((200,40), text="sample_text",fill="#000000")
        self.result_canvas.itemconfigure(self.rec_rolled_game,state="hidden")
        self.result_canvas.itemconfigure(self.text_rolled_game,state="hidden")
        
        #канвас для кнопок управляющих рулеткой
        self.btn_canvas=Canvas(width = 450, height = 20) 
        #создание кнопок и помещение их в канвас
        self.start_roll_button = Button(text="КРУТИ ЕБАТЬ!",command=self.start_roll)
        self.roll_again_button = Button(text="ДАЙ МНЕ ЕЩЕ!",command=self.start_roll)
        self.roll_again_button.config(state=DISABLED)
        self.mark_game_button = Button(text="Исключить игру из пула")
        #помещение кнопок управление рулеткой в канвас
        self.start_roll_button_btn=self.btn_canvas.create_window(10,0,anchor=NW,window=self.start_roll_button)
        self.roll_again_button_btn=self.btn_canvas.create_window(160,0,anchor=NW,window=self.roll_again_button)
        #self.result_canvas.itemconfigure(self.roll_again_button_btn,state = 'disabled')
        self.mark_game_button_btn=self.btn_canvas.create_window(310,0,anchor=NW,window=self.mark_game_button)
        
        #кнопка возвращениея на мейн окно
        self.go_back_btn = Button(text="Назад",command=self.get_back_to_main_window,padx=20,pady=10)
        
        #помещение элементов на окно программы
        self.btn_canvas.grid(column = 0,row = 3,columnspan=3)
        self.cnv_roulette.grid(column = 0,row = 1,columnspan=3)
        self.result_canvas.grid(column=0,row=2,columnspan=2)
        self.go_back_btn.grid(column=0,row = 4,columnspan=2,padx=20,pady=30)
        
        
        
    
    def start_roll(self):
        self.start_roll_button.config(state=DISABLED)
        self.roll_again_button.config(state=DISABLED)
        #убираем результаты прошлой рулетки, если они были
        for el in self.cnv_roulette.find_all():
            self.cnv_roulette.delete(el)
        self.result_canvas.itemconfigure(self.rec_rolled_game,state="hidden")
        self.result_canvas.itemconfigure(self.text_rolled_game,state="hidden")
        #инициализация доп. элементов рулетки
        velocity = self.start_velocity
        self.game_cells_list=self.create_game_cells(self.gm_cont.get_num_cells(),velocity)
        self.choice_line = self.cnv_roulette.create_line(self.gm_cont.get_choice_coord(),fill ="#eaf485",width = "4p",tags="choice_line")
        start_roulette_time = time.time()
        #for i in range(25):
        #цикл рулетки
        while(velocity>0):

            for cell in self.game_cells_list:
                if self.gm_cont.is_last_cell_need_to_delete(cell.get_top_side_y_coord()):
                    self.move_cell_to_top(cell) 
            self.move_cells()  
            time.sleep(0.02)
            #self.change_coords_in_list()
            #постепенно уменьшаем скорость всех ячеек
            if time.time()>=start_roulette_time+self.time_gap_to_reduce:
                start_roulette_time+=1
                velocity = self.slow_down_roulette(velocity)
                #print("THIS IS VELOCITY",velocity)
            self.window.update()
            #print("........................................")
        #если линия совпадает с границей ячейки, то прокрутить рулетку на несколько пунктов вниз
        #time.sleep(0.99)
        self.resolve_draw_situation()
        self.window.update()
        #выводим результат ролла на экран
        self.get_result_of_roll()
        #self.result_canvas.itemconfigure(self.roll_again_button_btn,state = 'normal')
        self.roll_again_button.config(state=NORMAL)
    
    def resolve_draw_situation(self):
        coord_of_choice_line = self.cnv_roulette.coords(self.choice_line)
        
        #troubleshoot
        print(f"This is choice line y coord {coord_of_choice_line[1]}")
        for el in self.cnv_roulette.find_all():
            if self.cnv_roulette.itemcget(el,"tags")!="choice_line":
                print(f"This is cell y coord {self.cnv_roulette.coords(el)[1]}. Potential DRAW:{abs(self.cnv_roulette.coords(el)[1]-coord_of_choice_line[1])}")

        if any(abs(self.cnv_roulette.coords(el)[1]-coord_of_choice_line[1])<=4 and self.cnv_roulette.itemcget(el,"tags")!="choice_line" and self.cnv_roulette.itemcget(el,"tags")!="text_block"  for el in self.cnv_roulette.find_all()):
            print("DRAW")
            for el in self.cnv_roulette.find_all():
                if self.cnv_roulette.itemcget(el,"tags")!="choice_line":
                    self.cnv_roulette.move(el,0,5)
    
    def create_game_cells(self,num_of_game_blocks,start_velocity):
        '''
        Метод для разметки координат всех клеток для начала прокрутки
        и создание списка объектов клеток
        '''
        temp_game_cell_list = []
        #получаем координаты первой клетки
        next_cell_coord = self.gm_cont.get_first_cell_coord()# формат left(x,y) right(x,y)
        #записываем клетки в массив клеток, так чтобы одна клетка была в ооб
        #в самой же рулетке в ооб будут находится 2 клетки, это необходимо для того чтобы не было видно как сверху спавнится 
        #новая клетка при каждой прокрутке колеса
        #записываем клетки игры в массив клеток
        for i in range(num_of_game_blocks+2):  
            game_param_dict = self.d_manager.pick_random_game()
            #print("this is game param_dict",game_param_dict)
            temp_game_cell_list.append(Game_cell(self.cnv_roulette,start_velocity,next_cell_coord,game_param_dict["game_name"],self.cell_colors[game_param_dict["game_rarity"]],self.gm_cont.get_cell_height()))
            next_cell_coord = [next_cell_coord[0],next_cell_coord[1]+self.gm_cont.get_cell_height(),next_cell_coord[2],next_cell_coord[3]+self.gm_cont.get_cell_height()]
        
        return list(temp_game_cell_list)
            
    
    def move_cells(self):
        '''
            метод сдвига всех клеток
        '''
        for cell in self.game_cells_list:
            cell.move()
    '''
    def change_coords_in_list(self):
        """
            меняет в объектах клеток координаты, вроде бы как лишний метод
        """
        for cell in self.game_cells_list:
            cell.change_current_coords()
    '''        
    
    def slow_down_roulette(self,velocity):
        '''
            метод постепенно замедляющий рулетку
            используется в main_loop
        '''
        velocity=velocity-self.reduce_vel_param
        for cell in self.game_cells_list:
            cell.change_velocity(velocity)
        return velocity
    
        
    def move_cell_to_top(self,cell):
        '''
            метод для перемещения самой нижней клетки наверх
            и назначение ей новой игры и цвета
        '''
        first_cell = self.get_first_visible_cell()#клетка которая сейчас находится наверху
        #print("this is obj of first cell",first_cell)
        coordinates_first_cell = self.cnv_roulette.coords(first_cell.rectangle_block) #получаем координаты клетки, которая наверху
        coordinates_first_cell = [coordinates_first_cell[0],coordinates_first_cell[1]-self.gm_cont.get_cell_height(),coordinates_first_cell[2],coordinates_first_cell[3]-self.gm_cont.get_cell_height()]
        #print("THIS IS FIRST CELL COORDS",coordinates_first_cell)
        
        game_param_dict = self.d_manager.pick_random_game() # снова выбираем игру, так как наверху будет обновленная клетка
        cell.move_cell_to_start(coordinates_first_cell,game_param_dict["game_name"],self.cell_colors[game_param_dict["game_rarity"]]) #передвигаем клетку наверх, вызывая ее метод
        
    def get_first_visible_cell(self):
        '''
            метод необходим для получения самой верхней видимой клетки
            относительно нее мы ставим клетку с новой игрой выше
        '''
        min_y=9999
        min_cell=None
        for cell in self.game_cells_list:
            if cell.get_top_side_y_coord()<min_y:
                min_y = cell.get_top_side_y_coord()
                min_cell=cell
        return min_cell 
        
    #отображение итога ролла
    '''
    def get_all_cells_coords(self):
        print("this is cells coords")
        for cell in game_cells_list:
            print(cell.get_coords())
    '''
    def get_result_of_roll(self):
        """
            получение результата ролла на основании ячеек
            и вывод его в блок-результата 
        """
        coord_of_choice_line = self.cnv_roulette.coords(self.choice_line)
        color=""
        name=""
        cnv_objects = self.cnv_roulette.find_all()
        for i in range(len(cnv_objects)):
            #print(self.cnv_roulette.itemcget(cell,"tags"))
            cnv_obj=cnv_objects[i]
            if self.cnv_roulette.itemcget(cnv_obj,"tags") == "game_block":
                
                if self.cnv_roulette.coords(cnv_obj)[1]<=coord_of_choice_line[1] and self.cnv_roulette.coords(cnv_obj)[3]>=coord_of_choice_line[1]:
                    color = self.cnv_roulette.itemcget(cnv_obj,"fill")
                    name = self.cnv_roulette.itemcget(cnv_objects[i+1],"text")
                    break

        self.result_canvas.itemconfigure(self.rec_rolled_game,fill=color,state="normal")
        self.result_canvas.itemconfigure(self.text_rolled_game,text=name ,state="normal")
        

    
    #возвратится назад на main_window 
    def get_back_to_main_window(self):
        self.cnv_roulette.grid_remove()
        self.btn_canvas.grid_remove()
        self.result_canvas.grid_remove()
        self.go_back_btn.grid_remove()
        self.Window_Controller.return_to_main_window()