import math
import random
from utils.config import COLUMN_COUNT
from utils.minimax import minimax
from utils.dqn_agent import DQNAgent
from utils.game_engine import Board


def get_minimax_move(board: Board, depth=4):
    result = minimax(board, depth, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, debug=True)
    col, _ = result[:2]
    valid_actions = [c for c in range(COLUMN_COUNT) if board.is_valid_location(c)]
    if col is None or col not in valid_actions:
        col = random.choice(valid_actions)
    return col


def get_dqn_move(agent: DQNAgent, board: Board):
    state = board.grid.flatten()
    valid_actions = [c for c in range(COLUMN_COUNT) if board.is_valid_location(c)]
    return agent.get_action(state, epsilon=0.0, valid_actions=valid_actions)