# utils/minimax.py:
import numpy as np
import math
from utils.config import ROW_COUNT, COLUMN_COUNT, WIN_COUNT, GRAY
from utils.game_engine import Board

PLAYER = 1
AI = 2
EMPTY = 0

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 1000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 50
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 10

    return score

def score_position(board: np.ndarray, piece: int) -> int:
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+WIN_COUNT]
            score += evaluate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+WIN_COUNT]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WIN_COUNT)]
            score += evaluate_window(window, piece)

    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r-i][c+i] for i in range(WIN_COUNT)]
            score += evaluate_window(window, piece)

    return score

def get_valid_locations(board: np.ndarray):
    return [c for c in range(COLUMN_COUNT) if board[ROW_COUNT-1][c] == 0]

def is_terminal_node(board_obj: Board):
    return board_obj.winning_move(PLAYER) or board_obj.winning_move(AI) or len(get_valid_locations(board_obj.grid)) == 0

def classify_move(board_obj: Board, piece: int) -> str:
    if board_obj.winning_move(piece):
        return "offensive (winning)"
    if count_winning_moves(board_obj, piece) >= 2:
        return "offensive (fork)"

    opponent = PLAYER if piece == AI else AI
    if count_winning_moves(board_obj, opponent) >= 2:
        return "defensive (block fork)"
    if board_obj.winning_move(opponent):
        return "defensive (block win)"

    return "neutral"

def minimax(board_obj: Board, depth, alpha, beta, maximizingPlayer, debug=False):
    valid_locations = get_valid_locations(board_obj.grid)
    terminal = is_terminal_node(board_obj)
    candidates = []

    if depth == 0 or terminal:
        if terminal:
            score = 1_000_000 if board_obj.winning_move(AI) else -1_000_000 if board_obj.winning_move(PLAYER) else 0
        else:
            score = score_position(board_obj.grid, AI)
        if debug:
            return (None, score, [])
        else:
            return (None, score)

        

    if maximizingPlayer:
        value = -math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = Board(grid=np.copy(board_obj.grid))
            row = temp_board.get_next_open_row(col)
            temp_board.drop_piece(row, col, AI)

            forks = count_winning_moves(temp_board, AI)
            if forks >= 2:
                return (col, 10000, [(col, 10000, "offensive (fork)")]) if debug else (col, 10000)

            _, new_score, _ = minimax(temp_board, depth-1, alpha, beta, False, debug)
            move_type = classify_move(temp_board, AI)
            candidates.append((col, new_score, move_type))

            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return (best_col, value, candidates) if debug else (best_col, value)

    else:
        value = math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = Board(grid=np.copy(board_obj.grid))
            row = temp_board.get_next_open_row(col)
            temp_board.drop_piece(row, col, PLAYER)

            forks = count_winning_moves(temp_board, PLAYER)
            if forks >= 2:
                return (col, -10000, [(col, -10000, "defensive (block fork)")]) if debug else (col, -10000)

            _, new_score, _ = minimax(temp_board, depth-1, alpha, beta, True, debug)
            move_type = classify_move(temp_board, PLAYER)
            candidates.append((col, new_score, move_type))

            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break

        return (best_col, value, candidates) if debug else (best_col, value)

def count_winning_moves(board_obj: Board, piece: int) -> int:
    count = 0
    for col in get_valid_locations(board_obj.grid):
        temp = Board(grid=np.copy(board_obj.grid))
        row = temp.get_next_open_row(col)
        temp.drop_piece(row, col, piece)
        if temp.winning_move(piece):
            count += 1
    return count
