

class Game_Control:
    '''
    класс нужен для контроля рулетки (канвас в котором крутятся ячейки) и ничего более
    объект Game_Control содержит какие-то дефолтные значения задаваемые в init
    - границы поля рулетеки (canvas-а)
    - 
    
    кажду новую партию рулетки будет вызывать метод, который из класса DataManager берет рандомные игры
    '''
    def __init__(self,cnv_width,cnv_height):
        self.right_coord=cnv_width #скорее всего не понадобится 
        self.top_coord =cnv_height
        self.number_of_cells=6
        self.number_of_actual_cells=self.number_of_cells+1
        self.choice_line_y_coord = self.top_coord/2
        
    #методы проверки нужности новой клетки и ненужности последней клетки в рулетке
    def is_new_cell_needed(self,bottom_side_cell_y_coord):
        if bottom_side_cell_y_coord>=self.top_coord:
            return True
        return False
        
    def is_last_cell_need_to_delete(self,top_side_cell_y_coord):
        if top_side_cell_y_coord>=self.top_coord:
            return True
        return False
    
    #метод для получения размера клетки в зависимости от размера поля
    def get_cell_height(self):
        return int(self.top_coord/self.number_of_cells)
        
    
    def get_first_cell_coord(self):
        '''
        получить координату клетки, которая будет вновь создана 
        и пока находится за пределами видимости
        '''
        first_cell_coord = [0,-(self.get_cell_height()),self.right_coord,0] # формат left(x,y) right(x,y)
        return first_cell_coord
        
    #получение списка игр, которые будут в текущем пуле рулетки
    def get_new_games_pool(self):
        return ["The Two Thrones","Prototype","popaww"]
        
    def get_num_cells(self):
        return self.number_of_cells
    
    def get_choice_coord(self):
        return [0,self.choice_line_y_coord,self.right_coord,self.choice_line_y_coord]