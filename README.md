# FirstGame_RL
This project uses a simple shooting game to create a custom Gymnasium environment in which a DQN agent is trained.
The game has two characters, a bot which makes random moves, and the controllable player which the agent learns to operate.
The goal of the game is to shoot and avoid getting hit, the first player to be hit 10 times loses.
The observation system of the environment collects information regarding each player's health, location, which attacks have hit and where any active attacks are currently.
The agent is rewarded 1 each time the opponent is hit, and penalized -1 each time it is hit. There is also a -0.1 penalty for missed shots to help the agent learn to aim. There is a +50 reward for winning and a -50 reward for losing.
