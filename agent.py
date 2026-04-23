'''This file will be for our tetris AI agent. It will use the heuristics file
   to calculate the best move for each piece iteration bsed on the heuristics listed
   (aggregate height, bumpiness, holes, lines cleares, ect. ).'''
from game import Game
from heuristics import Heuristics
import copy

class Agent :
    def __init__(self, weights = None) :
        self.heuristics = Heuristics(weights)

    # tries every possible move and scores each using the heuristics to find the best
    def choose_move(self, game) :
        highest_score = float('-inf')
        best_move = None

        for rotation in range(4) :
            for column in range(game.grid.num_cols) :
                simulate = self.simulate_move(game, rotation, column)
                if simulate is None:
                    continue

                score = self.heuristics.evaluate_board(simulate.grid)
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

        # shifts the block into the correct position
        while simulate.current_block.column_offset < column :
            simulate.current_block.move(0,1)
        while simulate.current_block.column_offset > column :
            simulate.current_block.move(0,-1)

        if not simulate.block_inside() or simulate.block_collide() :
            return None
 
        while True :
            simulate.current_block.move(1, 0)
            if not simulate.block_inside() or simulate.block_collide() :
                simulate.current_block.move(-1, 0)
                break
        
        if not simulate.block_inside() :
            return None

        simulate.lock_block()

        return simulate

    # executes the chosen move on the actual game
    def place_piece(self, game, rotation, column) :
        game.current_block.rotation_state = rotation
        game.current_block.column_offset = column
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
