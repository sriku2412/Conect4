# utils/train_dqn.py:
import numpy as np
import random
from utils.game_engine import Board
from utils.dqn_agent import DQNAgent
from utils.config import COLUMN_COUNT
import os


def opponent_wins_next(board, current_player):
    opponent = 3 - current_player
    grid = board.grid
    for col in range(COLUMN_COUNT):
        if grid[-1][col] == 0:
            temp = Board(grid=grid.copy())
            row = temp.get_next_open_row(col)
            temp.drop_piece(row, col, opponent)
            if temp.winning_move(opponent):
                return True
    return False


def train(episodes=50000, checkpoint_interval=5000):
    agent = DQNAgent(model_size='large', use_double_dqn=True)
    epsilon = 1.0
    epsilon_decay = 0.9997
    min_epsilon = 0.05

    for ep in range(1, episodes + 1):
        board = Board.create()
        current_player = 1
        state = board.grid.reshape(-1)
        done = False

        while not done:
            valid_actions = [c for c in range(COLUMN_COUNT) if board.grid[-1][c] == 0]
            action = agent.get_action(state, epsilon, valid_actions)

            row = board.get_next_open_row(action)
            board.drop_piece(row, action, current_player)

            next_state = board.grid.reshape(-1)
            reward = -0.01  # Default step penalty

            if board.winning_move(current_player):
                reward = 1.0
                done = True
            elif opponent_wins_next(board, current_player):
                reward = -1.0
            elif not any(board.grid[-1][c] == 0 for c in range(COLUMN_COUNT)):
                reward = 0.3
                done = True

            agent.remember(state, action, reward, next_state, done)
            agent.learn()
            state = next_state

        epsilon = max(min_epsilon, epsilon * epsilon_decay)

        if ep % 1000 == 0:
            print(f"Episode {ep}, Epsilon: {epsilon:.4f}")

        # check for temp folder
        if not os.path.exists("temp"):
            os.makedirs("temp")
            
        if ep % checkpoint_interval == 0:
            checkpoint_path = f"temp/dqn_model_{ep}.pth"
            agent.save(checkpoint_path)
            print(f"Checkpoint saved at episode {ep} -> {checkpoint_path}")

    agent.save("utils/dqn_model.pth")
    print("Training completed and final model saved.")


if __name__ == "__main__":
    train(episodes=50000)
