import pygame
import random
import math


class Game(object):
    def __init__(self):
        self.hit_sound = None
        self.goal_sound = None
        self.bounce_sound = None
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        self.menu_font = pygame.font.Font(None, 36)
        self.menu_options = ["Singleplayer", "Multiplayer"]
        self.selected_option = 0
        self.menu_done = False
        self.player = None
        self.enemy = None
        self.window = None
        self.ball = None
        self.score = {'player': 0, 'enemy': 0}
        self.game_over = False
        self.singleplayer_option_rect = pygame.Rect(150, 200, 200, 50)  # Rect for singleplayer option
        self.multiplayer_option_rect = pygame.Rect(150, 300, 200, 50)  # Rect for multiplayer option
        self.transparent_circle = None
        pygame.init()
        self.load_sounds()


    def load_sounds(self):
        self.hit_sound = pygame.mixer.Sound("hit.mp3")
        self.goal_sound = pygame.mixer.Sound("goal.mp3")
        self.bounce_sound = pygame.mixer.Sound("bounce.mp3")  # New sound effect for bouncing off other surfaces
        pygame.mixer.music.load("background_music.mp3")

    def play_hit_sound(self):
        self.hit_sound.play()

    def play_goal_sound(self):
        self.goal_sound.play()

    def play_bounce_sound(self):
        self.bounce_sound.play()

    def play_background_music(self):
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def run_menu(self):
        self.window = pygame.display.set_mode((500, 500))
        self.play_background_music()
        quit_button_rect = pygame.Rect(200, 400, 100, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.singleplayer_option_rect.collidepoint(mouse_pos):
                        self.start_singleplayer()
                        return
                    elif self.multiplayer_option_rect.collidepoint(mouse_pos):
                        self.start_multiplayer()
                        return

            self.draw_menu(quit_button_rect)  # Pass quit button rect to draw_menu method
            pygame.display.update()

    def draw_menu(self, quit_button_rect):
        self.window.fill((250, 255, 225))
        font = pygame.font.Font(None, 36)
        singleplayer_text = font.render("Singleplayer", True, (0, 0, 0))
        multiplayer_text = font.render("Multiplayer", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))  # Render quit button text
        pygame.draw.rect(self.window, (0, 0, 0), self.singleplayer_option_rect, 2)
        pygame.draw.rect(self.window, (0, 0, 0), self.multiplayer_option_rect, 2)
        pygame.draw.rect(self.window, (0, 0, 0), quit_button_rect, 2)  # Draw quit button rect
        self.window.blit(singleplayer_text, (180, 210))
        self.window.blit(multiplayer_text, (180, 310))
        self.window.blit(quit_text, (220, 410))  # Draw quit button text

    def start_singleplayer(self):
        self.window = pygame.display.set_mode((500, 500))
        self.player = Player(x=225, y=470)
        self.enemy = Enemy()
        self.ball = Ball(self.window)
        self.play_background_music()
        self.game_loop()

    def start_multiplayer(self):
        self.window = pygame.display.set_mode((500, 500))
        self.player = Player(x=225, y=470)
        self.player2 = Player(x=225, y=20)
        self.ball = Ball(self.window)
        self.play_background_music()
        self.game_loop()

    def game_loop(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            pygame.time.delay(10)

        pygame.quit()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if hasattr(self, 'player2'):
            if keys[pygame.K_a]:
                self.player2.move_left()
            if keys[pygame.K_d]:
                self.player2.move_right()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def draw(self):
        self.window.fill((250, 255, 225))
        self.draw_borders()
        self.draw_goal_areas()
        self.player.draw(self.window)
        if hasattr(self, 'player2'):
            self.player2.draw(self.window)
        else:
            self.enemy.draw(self.window)
        self.ball.draw()
        self.draw_score()

    def draw_borders(self):
        # Draw the first half of the top border
        pygame.draw.rect(self.window, (0, 0, 0), (0, 0, 200, 10))  # First half of top border

        # Draw the second half of the top border
        pygame.draw.rect(self.window, (0, 0, 0), (300, 0, 200, 10))  # Second half of top border
        pygame.draw.rect(self.window, (0, 0, 0), (0, 10, 10, 480))  # Left border
        pygame.draw.rect(self.window, (0, 0, 0), (490, 10, 10, 480))  # Right border
        pygame.draw.rect(self.window, (0, 0, 0), (0, 490, 200, 10))  # Bottom border
        pygame.draw.rect(self.window, (0, 0, 0), (300, 490, 200, 10))  # Bottom border

    def draw_goal_areas(self):
        pygame.draw.rect(self.window, (220, 220, 220), (200, 0, 100, 10))  # Top goal area
        pygame.draw.rect(self.window, (220, 220, 220), (200, 490, 100, 10))  # Bottom goal area

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        player_score_text = font.render(f"Player: {self.score['player']}", True, (0, 0, 0))
        enemy_score_text = font.render(f"Enemy: {self.score['enemy']}", True, (0, 0, 0))
        self.window.blit(player_score_text, (20, 20))
        self.window.blit(enemy_score_text, (350, 20))

    def update(self):
        if hasattr(self, 'player2'):
            self.player2.update()
        else:
            self.enemy.update(self.ball, self.player)
        self.player.update()
        self.ball.update()
        self.check_goal()
        self.ball.collide(self.player)
        if hasattr(self, 'player2'):
            self.ball.collide(self.player2)
        else:
            self.ball.collide(self.enemy)

        # Check if the ball collides with the enemy
        if self.ball.collide(self.enemy):
            self.play_hit_sound()  # Play hit sound effect
        elif self.ball.collide(self.player):
            self.play_hit_sound()  # Play hit sound effect
        elif hasattr(self, 'player2') and self.ball.collide(self.player2):
            self.play_hit_sound()  # Play hit sound effect
        else:
            if self.ball.collide_with_window(self.window):
                self.play_bounce_sound()

    def check_goal(self):
        if self.ball.y <= 10 and 200 <= self.ball.x <= 300:  # Top goal
            self.score['player'] += 1
            self.ball.reset()
            self.ball.y_speed = -abs(self.ball.y_speed)  # Ensure ball moves downwards
            self.play_goal_sound()  # Play goal sound effect
        elif self.ball.y >= 490 and 200 <= self.ball.x <= 300:  # Bottom goal
            self.score['enemy'] += 1
            self.ball.reset()
            self.ball.y_speed = abs(self.ball.y_speed)  # Ensure ball moves upwards
            self.play_goal_sound()  # Play goal sound effect


class Player(object):
    def __init__(self, x, y):
        self.window = None
        self.x = x
        self.y = y
        self.width = 50
        self.height = 10
        self.speed = 10

    def move_left(self):
        self.x -= self.speed
        if self.x < 10:  # Limit player movement within borders
            self.x = 10

    def move_right(self):
        self.x += self.speed
        if self.x + self.width > 490:  # Limit player movement within borders
            self.x = 490 - self.width

    def update(self):
        pass

    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, self.width, self.height))


class Ball(object):
    radius = 8
    initial_speed = 6  # Adjust initial speed as needed
    bounce_multiplier = 1.1  # Adjust bounce speed multiplier as needed

    def __init__(self, window):
        self.y = 250
        self.x = 250
        self.x_speed = random.choice([-1, 1]) * self.initial_speed
        self.y_speed = random.choice([-1, 1]) * self.initial_speed
        self.window = window
        self.reset()

    def collide_with_window(self, window):
        # Check collision with window boundaries
        if (self.x + self.radius > window.get_width() - 10 or
                self.x - self.radius < 10 or
                self.y + self.radius > window.get_height() - 10 or
                self.y - self.radius < 10):
            return True
        return False

    def reset(self):
        self.x = 250
        self.y = 250
        self.x_speed = random.choice([-1, 1]) * self.initial_speed
        self.y_speed = random.choice([-1, 1]) * self.initial_speed

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        if self.y_speed > 500 or self.x_speed > 500:
            self.reset()
        if self.y + self.radius > 490 or self.y - self.radius < 10:
            # Check if the ball is not in the goal areas
            if not (200 <= self.x <= 300 and (self.y - self.radius <= 10 or self.y + self.radius >= 490)):
                self.y_speed = -self.y_speed * self.bounce_multiplier  # Increase speed after bounce

        if self.x + self.radius > 490 or self.x - self.radius < 10:
            self.x_speed = -self.x_speed * self.bounce_multiplier  # Increase speed after bounce

    def draw(self):
        pygame.draw.circle(self.window, (0, 0, 0), (self.x, self.y), self.radius)

    def collide(self, obj):
        if (obj != None):
            if (self.x + self.radius > obj.x and
                    self.x - self.radius < obj.x + obj.width and
                    self.y + self.radius > obj.y and
                    self.y - self.radius < obj.y + obj.height):
                self.reflect(obj, )
                return True

    def reflect(self, obj):
        # print(isinstance(tuple,game.player))
        if hasattr(game, 'player2') and obj == game.player2:
            # Calculate the angle and speed of the ball's reflection based on the player's movement speed and angle
            player_center_x = obj.x + obj.width / 2
            relative_intersect_x = player_center_x - self.x
            normalized_intersect_x = relative_intersect_x / (obj.width / 2)
            bounce_angle = normalized_intersect_x * (math.pi / 3)
            self.x_speed = (math.sin(bounce_angle) * obj.speed / 1.5)
            self.y_speed = (math.cos(bounce_angle) * obj.speed / 1.5)
        elif isinstance(obj, Enemy):
            # Calculate the angle and speed of the ball's reflection based on the enemy's movement speed and angle
            enemy_center_x = obj.x + obj.width / 2
            relative_intersect_x = enemy_center_x - self.x
            normalized_intersect_x = relative_intersect_x / (obj.width / 2)
            bounce_angle = normalized_intersect_x * (math.pi / 3)
            self.x_speed = (math.sin(bounce_angle) * obj.speed / 1.5)
            self.y_speed = (math.cos(bounce_angle) * obj.speed / 1.5)
        elif hasattr(game, 'player') and obj == game.player:
            # Calculate the angle and speed of the ball's reflection based on the enemy's movement speed and angle
            enemy_center_x = obj.x + obj.width / 2
            relative_intersect_x = enemy_center_x - self.x
            normalized_intersect_x = relative_intersect_x / (obj.width / 2)
            bounce_angle = normalized_intersect_x * (math.pi / 3)
            self.x_speed = -(math.sin(bounce_angle) * obj.speed / 1.5)
            self.y_speed = -(math.cos(bounce_angle) * obj.speed / 1.5)


class Enemy(object):
    def __init__(self):
        self.window = None
        self.x = 225
        self.y = 20
        self.width = 50
        self.height = 10
        self.speed = 4
        self.last_hit_time = None  # Initialize last_hit_time to None

    def set_last_hit_time(self, time):
        self.last_hit_time = time

    def update(self, ball, player):
        # Predict the ball's position at the time it reaches the enemy's position
        if ball.y_speed != 0:
            time_to_reach_enemy = (self.y - ball.y) / ball.y_speed
            predicted_intersection_x = ball.x + time_to_reach_enemy * ball.x_speed
        else:
            predicted_intersection_x = ball.x

        # Calculate tolerance threshold
        tolerance = 5  # Adjust as needed

        # Move the enemy based on the direction of the ball's vertical speed
        if ball.y_speed < 0:  # Ball moving upwards
            if abs(predicted_intersection_x - (self.x + self.width / 2)) > tolerance:
                # Move towards the predicted intersection point
                if predicted_intersection_x < self.x + self.width / 2:
                    self.x -= self.speed
                elif predicted_intersection_x > self.x + self.width / 2:
                    self.x += self.speed

                # Ensure the enemy stays within the playing area
                if self.x < 10:
                    self.x = 10
                elif self.x + self.width > 490:
                    self.x = 490 - self.width
        elif ball.y_speed > 0:  # Ball moving downwards
            if abs(predicted_intersection_x - (self.x + self.width / 2)) > tolerance:
                # Move away from the predicted intersection point
                if predicted_intersection_x < self.x + self.width / 2:
                    self.x += self.speed
                elif predicted_intersection_x > self.x + self.width / 2:
                    self.x -= self.speed

                # Ensure the enemy stays within the playing area
                if self.x < 10:
                    self.x = 10
                elif self.x + self.width > 490:
                    self.x = 490 - self.width

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))


game = Game()
game.run_menu()
