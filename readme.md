# Connect 4 with Hybrid AI

This is a personal project aimed at building a competitive Connect 4 AI using a combination of **Minimax** and **Deep Q-Network (DQN)** reinforcement learning. It includes a fully playable Pygame-based GUI and training pipeline.

---

## 🎮 Gameplay Features

- Human vs AI mode
- DQN + Minimax hybrid AI decision-making
- Round-based score tracking
- Highlighting the winning 4 chips
- Smooth piece drop animation with delays
- Intuitive and colorful UI

---

## 🤖 AI Logic

### 1. **Minimax Algorithm**

- Used for deterministic, rule-based play
- Evaluates board states up to a set depth (default: 4)
- Considers maximizing AI and minimizing opponent moves

### 2. **Deep Q-Network (DQN)**

- Neural network-based agent
- Trained using reinforcement learning
- Learns from board states and rewards

#### DQN Architecture

- Input: Flattened board grid (6x7 = 42 cells)
- Layers:
  - `fc1`: 512 units
  - `fc2`: 256 units
  - `fc3`: 7 units (1 per column)
- Activation: ReLU

#### Training Logic

- Episodes: 50,000
- Exploration: Epsilon-greedy (decays over time)
- Rewards:
  - Win: `+1.0`
  - Opponent win next: `-1.0`
  - Draw: `+0.3`
  - Step penalty: `-0.01`
- Double DQN logic to reduce overestimation
- Checkpoint saved every 5,000 episodes

You can run training via:

```bash
python utils/train_dqn.py
```

---

## 🧠 Personal Result

I challenged my trained AI and managed to win **3–2** in a 5-round match. The AI is strong but beatable with smart play, especially when you learn its patterns.

---

## 🛠️ Tech Stack

- Python 3.10+
- Pygame for UI
- NumPy + PyTorch for DQN
- Pydantic for data validation

---

## 📁 Project Structure

```
├── main.py                # Entry point
├── engine.py              # Game loop and logic
├── events.py              # Input handling
├── app.py                 # Drawing and rendering
├── utils/
│   ├── config.py          # Game settings
│   ├── game_engine.py     # Board mechanics
│   ├── dqn_agent.py       # DQN model and agent
│   ├── train_dqn.py       # Training loop
│   └── minimax.py         # Minimax algorithm
```

---

## 🚀 To Run the Game

```bash
python main.py
```

Use mouse clicks to drop chips. Press `Q` to quit or `R` to restart scores.

---

## 📦 Requirements

```bash
pip install pygame torch numpy pydantic
```

---

## ✅ Future Enhancements

- AI-vs-AI mode
- Player vs online model
- Web interface using React + FastAPI
- Graphical heatmap for AI decision

---

## 👤 Author

Built with love and curiosity by a data science enthusiast determined to beat the machine at its own game.

---

Enjoy playing and improving the AI! 🧠🎯
