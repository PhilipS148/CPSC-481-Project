'''Covers the main game functionallity'''
from grid import Grid
from blocks import *
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
    
    # function to update the score
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 40
        elif lines_cleared == 2:
            self.score += 100
        elif lines_cleared == 3:
            self.score += 300
        elif lines_cleared == 4:
            self.score += 1200
        self.score += move_down_points

    # spawing random blocks
    def get_random_block(self) :
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    # User interface for game
    def draw(self,screen) :
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 270)
        else:
            self.next_block.draw(screen, 270, 270)

    # move functionallity 
    def move_left(self) :
        self.current_block.move(0,-1)
        if self.block_inside() == False or self.block_collide() == True :
            self.current_block.move(0,1)

    def move_right(self) :
        self.current_block.move(0,1)
        if self.block_inside() == False or self.block_collide() == True :
            self.current_block.move(0,-1)

    def move_down(self) :
        self.current_block.move(1,0)
        if self.block_inside() == False or self.block_collide() == True :
            self.current_block.move(-1,0)
            self.lock_block()
    
    # sets block in place
    def lock_block(self) :
        tiles = self.current_block.get_cell_position()
        locked_above = False

        for position in tiles :
            if position.row < 0:
                locked_above = True
                continue
            self.grid.cells[position.row][position.column] = self.current_block.id
        
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        
        if locked_above or self.block_collide() == True :
            self.game_over = True
            
        return rows_cleared
        
    # rotation logic      
    def rotate(self) :
        self.current_block.rotate()
        if self.block_inside() == False or self.block_collide() == True :
            self.current_block.undo_rotate()

    # ensurs bound checking making sure the block does not go outside the grid
    def block_inside(self) :
        tiles = self.current_block.get_cell_position()
        for tile in tiles :
            if tile.column < 0 or tile.column >= self.grid.num_cols :
                return False
            if tile.row >= self.grid.num_rows :
                return False
        return True
    
    # collision detection making sure block sit ontop of each other and don't go through eachother 
    def block_collide(self) :
        tiles = self.current_block.get_cell_position()
        for tile in tiles :
            if tile.column < 0 or tile.column >= self.grid.num_cols :
                return True
            if tile.row >= self.grid.num_rows :
                return True
            if tile.row >= 0 and self.grid.is_cell_empty(tile.row, tile.column) == False :
                return True
        return False
    
    def reset(self) :
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
