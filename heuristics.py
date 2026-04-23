'''Heuristics:
   This file will cover the heuristics for are AI agent
        - lines cleares
        - holes
        - aggregate height
        - max_height
        - bumpiness
        - tetris bouns
    these heuristics will be used to guide the AI into making the best decision based
    on the board state.'''
from grid import Grid

class Heuristics:
    def __init__(self, weights = None):
        self.weights = weights if weights is not None else [1,-0.5, -0.5,-0.5]

    def evaluate_board(self, board):
        score = 0

        height = self.aggregate_height(board)
        lines = self.cleared_lines(board)
        holes = self.hole_count(board)
        bumpiness = self.bumpiness(board)


        score += 1 * lines
        score -= 0.5 * height
        score -= 0.5 * holes
        score -= 0.5 * bumpiness

        return score

    def column_heights(self, board) :
        heights = []
        for column in range(board.num_cols) :
            h = 0
            for row in range(board.num_rows) :
                if board.cells[row][column] != 0 :
                    h = board.num_rows - row
                    break
            heights.append(h)
        
        return heights

    def aggregate_height(self, board) :
        heights = self.column_heights(board)
        return sum(heights)

    def hole_count(self, board) :
        holes = 0
        for column in range(board.num_cols) :
            block_found = False
            for row in range(board.num_rows) :
                if board.cells[row][column] != 0 :
                    block_found = True
                elif block_found :
                    holes += 1
        return holes

    def bumpiness(self, board) :
        heights = self.column_heights(board)
        total_bumpiness = 0

        for i in range(len(heights) - 1):
            total_bumpiness += abs(heights[i] - heights[i + 1])

        return total_bumpiness

    def cleared_lines(self, board) :
        lines_full = 0

        #below is basically just our is_row_full() method in grid, but using row in range instead of columns
    
        #loop just goes row by row (outer loop), then just checks every column(inner loop)
        for row in range(board.num_rows):
            full = True
            for column in range(board.num_cols):
                if board.cells[row][column] == 0: 
                    full = False
                    break
            if full:
                lines_full += 1 
        return lines_full
    
