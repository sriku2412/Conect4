# utils/evaluate_dqn.py:
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import torch
from utils.game_engine import Board
from utils.dqn_agent import DQNAgent
from utils.config import COLUMN_COUNT

def plot_q_values(agent, board: Board):
    state = board.grid.flatten()
    state_tensor = torch.FloatTensor(state).unsqueeze(0)
    with torch.no_grad():
        q_values = agent.model(state_tensor).squeeze().numpy()

    # Mask invalid actions with NaN
    valid_actions = [c for c in range(COLUMN_COUNT) if board.is_valid_location(c)]
    q_masked = np.full_like(q_values, np.nan)
    for c in valid_actions:
        q_masked[c] = q_values[c]

    plt.figure(figsize=(8, 2))
    sns.heatmap([q_masked], annot=True, fmt=".2f", cmap="coolwarm", cbar=True,
                xticklabels=[str(i) for i in range(COLUMN_COUNT)], yticklabels=[])
    plt.title("Q-values per Column")
    plt.xlabel("Column")
    plt.tight_layout()
    plt.show()

def evaluate(agent, episodes=100):
    win, loss, draw = 0, 0, 0
    results = []

    for ep in range(1, episodes + 1):
        board = Board.create()
        state = board.grid.flatten()
        current_player = 1
        done = False

        if ep <= 5:
            print(f"\nEpisode {ep} — Initial Q-values:")
            plot_q_values(agent, board)

        while not done:
            valid_actions = [c for c in range(COLUMN_COUNT) if board.is_valid_location(c)]

            if current_player == 1:
                action = agent.get_action(state, epsilon=0.0, valid_actions=valid_actions)
            else:
                action = random.choice(valid_actions)  # Random opponent

            row = board.get_next_open_row(action)
            board.drop_piece(row, action, current_player)

            if board.winning_move(current_player):
                done = True
                if current_player == 1:
                    win += 1
                    results.append("Win")
                else:
                    loss += 1
                    results.append("Loss")
            elif board.is_full():
                done = True
                draw += 1
                results.append("Draw")
            else:
                current_player = 3 - current_player
                state = board.grid.flatten()

    print(f"\nOut of {episodes} games:\nWins: {win}\nLosses: {loss}\nDraws: {draw}")
    plot_results(results)

def plot_results(results):
    counts = {
        "Win": results.count("Win"),
        "Loss": results.count("Loss"),
        "Draw": results.count("Draw")
    }
    plt.figure(figsize=(6, 4))
    plt.bar(counts.keys(), counts.values())
    plt.title("DQN Agent Performance")
    plt.ylabel("Number of Games")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    agent = DQNAgent()
    agent.load("utils/dqn_model.pth")
    evaluate(agent, episodes=100)
