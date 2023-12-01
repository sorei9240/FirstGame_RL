import gymnasium as gym
import numpy as np
from model import DQLAgent
import pygame
import torch

# Create an instance of the environment
env = gym.make('hVisFirstGameEnv-v0')

# Get the size of state and action spaces
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# DQL agent instance
agent = DQLAgent(state_size, action_size)

# Training parameters
num_episodes = 250  # Number of episodes to train
batch_size = 32 # Batch size for experience replay

# Render training
render_training = True

for episode in range(num_episodes):
    state, info = env.reset()  # Reset the environment
    state = np.reshape(state, [1, state_size]).astype(np.float32)
    total_reward = 0

    for time in range(500):  # Maximum steps per episode
        for event in pygame.event.get(): # Prevent the game from freezing
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        action = agent.act(state)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
        if render_training:
            env.render()

        if done:
            print(f"Episode: {episode+1}/{num_episodes}, Score: {total_reward}, Epsilon: {agent.epsilon}")
            break
        # Train the agent with experience replay
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

    # Adjust epsilon for exploration/exploitation balance
    if agent.epsilon > agent.epsilon_min:
        agent.epsilon *= agent.epsilon_decay
    
torch.save(agent.model.state_dict(), 'trained_dqn_model.pt')
print("Model saved as trained_dqn_model.pt")
print("Training completed!")
env.close()