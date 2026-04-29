'''This file will be for our tetris AI agent. It will use the heuristics file
   to calculate the best move for each piece iteration bsed on the heuristics listed
   (aggregate height, bumpiness, holes, lines cleares, ect. ).'''
from game import Game
from heuristics import Heuristics
import copy

class Agent :
    def __init__(self, weights) :
        self.heuristics = Heuristics(weights)

    # tries every possible move and scores each using the heuristics to find the best
    def choose_move(self, game) :
        highest_score = float('-inf')
        best_move = None

        for rotation in range(4) :
            for column in range(game.grid.num_cols) :
                result = self.simulate_move(game, rotation, column)

                if result is None:
                    continue
                    
                simulate, rows_cleared = result

                score = self.heuristics.evaluate_board(simulate.grid, rows_cleared)
                if score > highest_score :
                    highest_score = score
                    best_move = (rotation, column)

        return best_move
    
    # simulates moves for the current piece and board state
    def simulate_move(self, game, rotation, column) :
        # copies the current game state
        simulate = Game()
        simulate.grid.cells = copy.deepcopy(game.grid.cells)
        simulate.current_block = copy.deepcopy(game.current_block)
        simulate.next_block = copy.deepcopy(game.next_block)
        
        simulate.current_block.rotation_state = rotation 

        col_values = []
        for pos in simulate.current_block.cells[rotation] :
            col_values.append(pos.column)
        
        min_cell_col = min(col_values)
        simulate.current_block.column_offset = column - min_cell_col

        if not simulate.block_inside() or simulate.block_collide():
            return None

        while True :
            simulate.current_block.move(1, 0)
            if not simulate.block_inside() or simulate.block_collide() :
                simulate.current_block.move(-1, 0)
                break
        
        if not simulate.block_inside() :
            return None

        rows_cleared = simulate.lock_block()

        return simulate, rows_cleared

    # executes the chosen move on the actual game
    def place_piece(self, game, rotation, column) :
        game.current_block.rotation_state = rotation
        
        col_values = []
        for pos in game.current_block.cells[rotation] :
            col_values.append(pos.column)
        
        min_cell_col = min(col_values)
        game.current_block.column_offset = column - min_cell_col

        original_block = game.current_block
        
        while game.current_block is original_block and not game.game_over :
           game.move_down()

    def run_game(self, game) :
        if game.game_over :
            return False

        best_move = self.choose_move(game)
        if best_move is None :
            game.game_over = True
            return False
         
        rotation = best_move[0]
        column = best_move[1]
        self.place_piece(game, rotation, column)
        
        return True
