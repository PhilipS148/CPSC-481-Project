from grid import Grid

#Not working heuristics yet, just setting stuff up


#This is just like the evalution method, we can just make it call the heuristics we'll come up with inside
#The board arg will just be the board we end up with per placement(including rotations n stuff)

def evaluate_board(board):
    score = 0

    #the 4 heuristic functions we talked about before (make later)
    lines = cleared_lines(board)
    height = aggregate_height(board)
    holes = hole_count(board)
    bumpiness = bumpiness(board)

    #then from those 4 heuristics, they'll affect the score variable, so like:
    score += 1.0 * lines
    score -= 0.5 * height
    score -= 0.5 *holes
    score -= 0.5 *bumpiness

    return score

def column_heights(board) :
    heights = []
    for column in range(board.num_cols) :
        h = 0
        for row in range(board.num_rows) :
            if board.grid[row][column] != 0 :
                h = board.num_rows - row
                break
        heights.append(h)
    return heights

def aggregate_height(board) :
    heights = column_heights(board)
    return sum(heights)

def hole_count(board) :
    holes = 0
    for column in range(board.num_cols) :
        block_found = False
        for row in range(board.num_rows) :
            if board.grid[row][column] != 0 :
                block_found = True
            elif block_found :
                holes += 1
    return holes

def bumpiness(board) :
    ''''''

def cleared_lines(board) :
    ''''''