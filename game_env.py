import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game import FirstGame
from gymnasium import spaces

class FirstGameEnv(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 60}
    def __init__(self):
        super(FirstGameEnv, self).__init__()
        self.game = FirstGame()

        # Define the action and observation spaces
        self.action_space = spaces.Discrete(5)  # 5 actions: left, right, up, down, shoot
        self.observation_space = spaces.Box(
            low=np.array([0]*38), 
            high=np.array([self.game.WIDTH, self.game.HEIGHT, 100, 1]*2 + [self.game.WIDTH, self.game.HEIGHT, 1]*10),
            dtype=np.float32
        )

        # Previous healh states to calculate reward
        self.previous_yellow_health = self.game.yellow_health
        self.previous_red_health = self.game.red_health
    
    # collect info about observation space
    def get_observation(self):
        yellow_state = [
            self.game.yellow.x, self.game.yellow.y, 
            self.game.yellow_health, 
            0 if self.game.yellow_facing_left else 1
        ]
        red_state = [
            self.game.red.x, self.game.red.y, 
            self.game.red_health, 
            0 if self.game.red_facing_left else 1
        ]
        attacks_info = self.game.get_attacks_info() 
        observation = np.array(yellow_state + red_state + attacks_info)
        print(self.yellow_state, self.red_state)
        return observation.astype(np.float32)
    def update_game_state(self):
        if self.game.bot_move_cooldown > 0:
            self.game.bot_move_cooldown -= 1
        if self.game.bot_shoot_cooldown > 0:
            self.game.bot_shoot_cooldown -= 1
        

    def step(self, action):
        done = False
        current_red_attacks_count = len(self.game.red_attacks)

        # Game logic
        bot_action = self.game.bot_choose_action()
        if bot_action in ['left', 'right', 'up', 'down']:
            self.game.bot_movement(bot_action)
        elif bot_action == 'shoot':
            self.game.bot_shoot(bot_action)
        self.game.check_hits()

        if action < 4:
            self.game.ai_handle_red_movement(action)
        elif action == 4:
            self.game.ai_handle_red_shooting(action)
        
        self.update_game_state()

        # Calculate reward
        reward = 0
        reward += (self.game.yellow_health - self.previous_yellow_health)
        reward -= (self.game.red_health - self.previous_red_health)

        new_attacks_count = len(self.game.red_attacks)
        missed_shots = current_red_attacks_count - new_attacks_count
        if new_attacks_count > current_red_attacks_count:
            for attack in self.game.red_attacks[-(new_attacks_count - current_red_attacks_count):]:
                if not attack.has_hit:
                    missed_shots += 1

        penalty_per_missed_shot = 0.1
        reward -= missed_shots * penalty_per_missed_shot

        game_win_reward = 50
        game_lose_penalty = -50

        if self.game.red_health <= 0:
            reward += game_lose_penalty
            done = True
        elif self.game.yellow_health <= 0:
            reward += game_win_reward
            done = True
        
        # Update health states
        self.previous_yellow_health = self.game.yellow_health
        self.previous_red_health = self.game.red_health


        # Prepare observation
        observation = self.get_observation()
        terminated = done 
        truncated = False 
        info = {} 
        return observation, reward, terminated, truncated, info

    
    # Reset the game
    def reset(self, seed=None, options=None):
        self.game.reset_game()
        self.previous_yellow_health = self.game.yellow_health
        self.previous_red_health = self.game.red_health
        observation = self.get_observation()
        info = {} 
        return observation, info
    
    def render(self, mode='human'):
        if mode == 'human':
            self.game.draw_window()
    
    def close(self):
        self.game.close_game()

from gymnasium.envs.registration import register

register(
    id='hVisFirstGameEnv-v0',
    entry_point='game_env:FirstGameEnv',
    max_episode_steps=1000,
)
