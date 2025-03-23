# utils/dqn_agent.py:
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
from utils.config import ROW_COUNT, COLUMN_COUNT
import os


class DQN(nn.Module):
    def __init__(self, model_size="default"):
        super(DQN, self).__init__()
        if model_size == "large":
            self.fc1 = nn.Linear(ROW_COUNT * COLUMN_COUNT, 512)
            self.fc2 = nn.Linear(512, 256)
            self.fc3 = nn.Linear(256, COLUMN_COUNT)
        else:
            self.fc1 = nn.Linear(ROW_COUNT * COLUMN_COUNT, 256)
            self.fc2 = nn.Linear(256, 128)
            self.fc3 = nn.Linear(128, COLUMN_COUNT)

    def forward(self, x):
        x = x.view(-1, ROW_COUNT * COLUMN_COUNT)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


class DQNAgent:
    def __init__(self, gamma=0.95, lr=0.001, batch_size=64, memory_size=10000, 
                 model_size="default", use_double_dqn=False):
        self.model = DQN(model_size=model_size)
        self.target_model = DQN(model_size=model_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size
        self.gamma = gamma
        self.learn_step = 0
        self.target_update_freq = 100
        self.use_double_dqn = use_double_dqn

        self.update_target()

    def get_action(self, state, epsilon, valid_actions=None):
        if valid_actions is None:
            valid_actions = list(range(COLUMN_COUNT))

        if random.random() < epsilon:
            return random.choice(valid_actions)

        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state_tensor).squeeze()

        mask = torch.full((COLUMN_COUNT,), float('-inf'))
        for a in valid_actions:
            mask[a] = q_values[a]

        return torch.argmax(mask).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def learn(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones).unsqueeze(1)

        curr_q = self.model(states).gather(1, actions)

        with torch.no_grad():
            if self.use_double_dqn:
                best_actions = self.model(next_states).argmax(1).unsqueeze(1)
                next_q = self.target_model(next_states).gather(1, best_actions)
            else:
                next_q = self.target_model(next_states).max(1)[0].unsqueeze(1)

        expected_q = rewards + (1 - dones) * self.gamma * next_q

        loss = nn.functional.mse_loss(curr_q, expected_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.learn_step += 1
        if self.learn_step % self.target_update_freq == 0:
            self.update_target()

    def update_target(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def save(self, path="utils/dqn_model.pth"):
        torch.save(self.model.state_dict(), path)

    def load(self, path="utils/dqn_model.pth"):
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path))
            self.update_target()
            print(f"Loaded trained model from {path}")
        else:
            print(f"[Warning] Model file '{path}' not found. Starting with untrained weights.")