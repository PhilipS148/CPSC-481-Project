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