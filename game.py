import pygame
import os
import random


class Attack:
    def __init__(self, x, y, direction, width, height):
        self.x = x
        self.y = y
        self.direction = direction
        self.vel = 10
        self.has_hit = False
        self.is_active = True
        self.width = width
        self.height = height

    def move(self):
        self.x += self.vel if self.direction == "right" else -self.vel
   
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 10, 5)
    
    def update(self):
        self.move()
        if self.x < 0 or self.x > self.width:
            self.is_active = False

class FirstGame:
    def __init__(self):
        # Constants
        self.WIDTH, self.HEIGHT = 900, 500
        self.FPS = 60
        self.VEL = 3
        self.SPRITE_WIDTH, self.SPRITE_HEIGHT = 90, 90
        self.bot_move_cooldown = 60
        self.bot_shoot_cooldown = random.randint(30, 120)
        self.bot_direction = "right"
        state_size = 38 
        action_size = 5 

        # Initialize Pygame Window
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("First Game!")

        # Load Assets
        self.KOTA_IMAGE = pygame.image.load(os.path.join("Assets", "kota.png")).convert_alpha()
        self.KOTA_FLIPPED = pygame.transform.flip(self.KOTA_IMAGE, True, False)
        self.KOTA = pygame.transform.scale(self.KOTA_FLIPPED, (self.SPRITE_WIDTH, self.SPRITE_HEIGHT))

        self.RAKITO_IMAGE = pygame.image.load(os.path.join("Assets", "rakito.png")).convert_alpha()
        self.RAKITO = pygame.transform.scale(self.RAKITO_IMAGE, (self.SPRITE_WIDTH, self.SPRITE_HEIGHT))

        self.BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "background.png")).convert_alpha()
        self.BACKGROUND = pygame.transform.scale(self.BACKGROUND_IMAGE, (self.WIDTH, self.HEIGHT))

        # Game State Variables
        self.yellow_facing_left = False
        self.red_facing_left = True
        self.yellow_attacks = []
        self.red_attacks = []
        self.reset_game()

    def reset_game(self):
        # Reset Game State
        self.red = pygame.Rect(700, 300, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)
        self.yellow = pygame.Rect(100, 300, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)
        self.red_health = 10
        self.yellow_health = 10
        self.red_attacks = []
        self.yellow_attacks = []
        self.bot_move_cooldown = 0
        self.bot_shoot_cooldown = random.randint(30, 120)

    def draw_window(self):
        # Draw Display
        self.WIN.blit(self.BACKGROUND, (0, 0))
        for attack in self.yellow_attacks:
            pygame.draw.rect(self.WIN, (255, 255, 0), (attack.x, attack.y, 10, 5))
        for attack in self.red_attacks:
            pygame.draw.rect(self.WIN, (255, 0, 0), (attack.x, attack.y, 10, 5))
        self.WIN.blit(self.KOTA, (self.yellow.x, self.yellow.y))
        self.WIN.blit(self.RAKITO, (self.red.x, self.red.y))
        pygame.display.update()

    def sprite_attack(self, x, y, direction, attacks):
        new_attack = Attack(x, y, direction, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)
        attacks.append(new_attack)
    
    def bot_choose_action(self):
        actions = []
        if self.bot_move_cooldown <= 0:
            actions.extend(['left', 'right', 'up', 'down'])
        if self.bot_shoot_cooldown <= 0:
            actions.append('shoot')

        if actions:
            chosen_action = random.choice(actions)
            if chosen_action != 'shoot':
                self.bot_move_cooldown = 10
            else:
                self.bot_shoot_cooldown = random.randint(30, 120)
            return chosen_action
        return None
    
    def bot_movement(self, bot_action):
        if bot_action in ['left', 'right', 'up', 'down']:
            if bot_action == "left" and self.yellow.x - self.VEL > 0:
                if not self.yellow_facing_left:
                    self.yellow_facing_left = True
                    self.KOTA = pygame.transform.flip(self.KOTA, True, False)
                self.yellow.x -= self.VEL
            elif bot_action == "right" and self.yellow.x + self.VEL + self.SPRITE_WIDTH < self.WIDTH:
                if self.yellow_facing_left:
                    self.yellow_facing_left = False
                    self.KOTA = pygame.transform.flip(self.KOTA, True, False)
                self.yellow.x += self.VEL
            elif bot_action == "up" and self.yellow.y - self.VEL > 0:
                self.yellow.y -= self.VEL
            elif bot_action == "down" and self.yellow.y + self.VEL + self.SPRITE_HEIGHT < self.HEIGHT:
                self.yellow.y += self.VEL
    
    def bot_shoot(self, bot_action):
        if self.bot_shoot_cooldown <= 0 and bot_action == 'shoot':
            direction = "left" if self.yellow_facing_left else "right"
            shot_x = self.yellow.x if self.yellow_facing_left else self.yellow.x + self.SPRITE_WIDTH - 10
            self.sprite_attack(shot_x, self.yellow.y, direction, self.yellow_attacks)
            self.bot_shoot_cooldown = random.randint(30, 120)
            print("Bot Shot Fired")
    
    def ai_handle_red_movement(self, action):
        if action == 0 and self.red.x - self.VEL > 0:  # Move Left
            if not self.red_facing_left:
                self.red_facing_left = True
                self.RAKITO = pygame.transform.flip(self.RAKITO, True, False)
            self.red.x -= self.VEL
        elif action == 1 and self.red.x + self.VEL + self.SPRITE_WIDTH < self.WIDTH:  # Move Right
            if self.red_facing_left:
                self.red_facing_left = False
                self.RAKITO = pygame.transform.flip(self.RAKITO, True, False)
            self.red.x += self.VEL
        elif action == 2 and self.red.y - self.VEL > 0:  # Move Up
            self.red.y -= self.VEL
        elif action == 3 and self.red.y + self.VEL + self.SPRITE_HEIGHT < self.HEIGHT:  # Move Down
            self.red.y += self.VEL
    
    def ai_handle_red_shooting(self, action):
        if action == 4:  # Shoot
            direction = "left" if self.red_facing_left else "right"
            shot_x = self.red.x if self.red_facing_left else self.red.x + self.SPRITE_WIDTH - 10
            self.sprite_attack(shot_x, self.red.y, direction, self.red_attacks)

    def check_hits(self):
        for attack in self.yellow_attacks + self.red_attacks:
            attack.update()
            if attack.is_active:
                if not attack.has_hit and (self.yellow.colliderect(attack.get_rect()) or self.red.colliderect(attack.get_rect())):
                    attack.has_hit = True
                    if attack in self.yellow_attacks:
                        self.red_health -= 1
                    else:
                        self.yellow_health -= 1
            else:
                if attack in self.yellow_attacks:
                    self.yellow_attacks.remove(attack)
                elif attack in self.red_attacks:
                    self.red_attacks.remove(attack)

    def get_ai_action(self):
        return random.randint(0, 4)

    def get_attacks_info(self):
        info = []
        for attack in self.yellow_attacks[:5]: 
            info.extend([attack.x, attack.y, 1 if attack.has_hit else 0])
        while len(info) < 5 * 3:  # 3 values per attack (x, y, has_hit)
            info.extend([0, 0, 0])

        for attack in self.red_attacks[:5]: 
            info.extend([attack.x, attack.y, 1 if attack.has_hit else 0])
        while len(info) < 10 * 3:  # 10 attacks in total (5 yellow + 5 red)
            info.extend([0, 0, 0])
        return info
    
    def close_game(self):
        pygame.quit()

    def main(self):
        clock = pygame.time.Clock()
        run = True
        self.bot_move_cooldown = 0
        self.bot_shoot_cooldown = 0

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Game logic
            if self.bot_move_cooldown > 0:
                self.bot_move_cooldown -= 1
            if self.bot_shoot_cooldown > 0:
                self.bot_shoot_cooldown -= 1

            bot_action = self.bot_choose_action()
            if bot_action in ['left', 'right', 'up', 'down']:
                self.bot_movement(bot_action)
                print(f"Bot Moved {bot_action}")
            elif bot_action == 'shoot':
                self.bot_shoot(bot_action)
                print("Bot Shot Fired")

            self.check_hits()

            action = self.get_ai_action()
            if action < 4:
                self.ai_handle_red_movement(action)
            elif action == 4:
                self.ai_handle_red_shooting(action)

            if self.yellow_health <= 0 or self.red_health <= 0:
                self.reset_game()

            self.draw_window()

        self.close_game()

if __name__ == "__main__":
    game = FirstGame()
    game.main()
