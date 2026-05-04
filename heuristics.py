'''
Heuristics:
   This file will cover the heuristics for are AI agent
        - lines cleares
        - holes
        - aggregate height
        - bumpiness
    these heuristics will be used to guide the AI into making the best decision based
    on the board state.
    
'''
from grid import Grid

class Heuristics:
    def __init__(self, weights):
        self.weights = weights 

    # function used to evaluate where a piece should be placed based on heuristics
    def evaluate_board(self, board, rows_cleared):
        
        w_lines, w_height, w_holes, w_bumpiness, w_max_height = self.weights

        height = self.aggregate_height(board)
        holes = self.hole_count(board)
        bumpiness = self.bumpiness(board)

        max_height = self.max_height(board)
        
        score = 0
        score += w_lines * rows_cleared
        score += w_height * height
        score += w_holes * holes
        score += w_bumpiness * bumpiness

        #possible new weight?
        score += w_max_height * max_height

        return score

    # calculate the column height of the current board state 
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

    # sums up the total height
    def aggregate_height(self, board) :
        heights = self.column_heights(board)
        return sum(heights)

    # counts how many open spaces there are on the board
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

    # measure the difference in height between adjacent columns
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
    
    def max_height(self, board):
        heights = self.column_heights(board)

        return max(heights)