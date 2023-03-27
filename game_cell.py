

class Game_cell:
    BG_COLOR = "#00ff59"
    def __init__(self,canvas,yVelocity,start_coordinates,game_name,color,cell_width):
        #эти координаты используются только при инициализации rectangle_block и game_name_label
        #далее используем координаты, которые хранятся прямо в объектах tkinter
        self.x_top_left = start_coordinates[0]
        self.y_top_left = start_coordinates[1]
        self.x_botton_right = start_coordinates[2]
        self.y_bottom_right = start_coordinates[3] 
        
        #характеристики внешности
        self.game_name = game_name
        self.bg_color = color
        self.cell_width=cell_width
        
        #скорость движения объекта
        self.xVelocity = 0
        self.yVelocity = yVelocity
        # канвас рулетки из gui_control
        self.canvas = canvas
        
        self.rectangle_block = self.canvas.create_rectangle(self.x_top_left,self.y_top_left,self.x_botton_right,self.y_bottom_right,fill=self.bg_color,outline="#FFFFFF",tags="game_block")
        self.game_name_label = self.canvas.create_text((self.x_botton_right/2,self.y_top_left+(self.cell_width)/2 ), text=self.game_name,fill="#FFFFFF",tags="text_block")
        #print("obj type",type(self.rectangle_block))

        
    def move(self):
        coordinates2 = self.canvas.coords(self.rectangle_block)
        #coordinates1 = self.canvas.coords(self.game_name_label)
        #print("text_cooords",coordinates1)
        #print("rectangle_block_coord and game",coordinates2,self.game_name)
        #print(self.game_name,self.bg_color)
        
        self.canvas.move(self.rectangle_block,self.xVelocity,self.yVelocity)
        self.canvas.move(self.game_name_label,self.xVelocity,self.yVelocity)
        
    def get_game_block_coord(self):
        #returns rectangle coords as such list - [x_top_left,y_top_left,x_bottom_right,y_bottom_right]
        return self.canvas.coords(self.rectangle_block)

    '''  
    def change_current_coords(self):
        current_coords = self.canvas.coords(self.rectangle_block)
        self.x_top_left = current_coords[0]
        self.y_top_left = current_coords[1]
        self.x_botton_right = current_coords[2]
        self.y_bottom_right = current_coords[3] 
    '''

    def get_coords(self):
        return self.canvas.coords(self.rectangle_block)
    
    def get_top_side_y_coord(self):
        coordinates = self.canvas.coords(self.rectangle_block)
        return coordinates[1]
        
    def get_botton_side_y_coord(self):
        coordinates = self.canvas.coords(self.rectangle_block)
        return coordinates[3]
        
    
    def change_velocity(self,new_velo):
        self.yVelocity=new_velo
    
    def move_cell_to_start(self,coords,game_name,game_rarity):
        self.canvas.itemconfigure(self.rectangle_block,state="hidden")# скрываем оба блока текста и ячейки
        self.canvas.itemconfigure(self.game_name_label,state="hidden")# скрываем оба блока текста и ячейки
        
        self.canvas.coords(self.rectangle_block,coords) # передвигаем блок над первым блоком
        #self.change_current_coords()
        self.canvas.coords(self.game_name_label,self.get_game_block_coord()[2]/2,self.get_game_block_coord()[1]+(self.cell_width)/2) #передвигаем текст в центр передвинутого блока
        
        #меняем параметры цвета/названия клетеки
        self.canvas.itemconfigure(self.game_name_label,text=game_name)
        self.canvas.itemconfigure(self.rectangle_block,fill=game_rarity)
        
        
        #восстанавливаем видимость виджетов
        self.canvas.itemconfigure(self.game_name_label,state="normal")
        self.canvas.itemconfigure(self.rectangle_block,state="normal")
        
    
    def remove_cell(self):
        self.canvas.delete(self.game_name_label)
        self.canvas.delete(self.rectangle_block)