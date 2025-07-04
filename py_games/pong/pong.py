import pygame
import sys
import math  # Import the math module

# Initialize Pygame
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5  # Initial vertical speed
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
WINNING_SCORE = 5
WALL_THICKNESS = 20
MAX_REFLECT_ANGLE = 75  # Maximum reflection angle in degrees


# --- Classes ---
class Paddle:
    """Represents a player's paddle."""

    def __init__(self, x, y):
        """Initializes the paddle at the given position."""
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        """Moves the paddle up or down, constrained by the screen bounds."""
        self.rect.y += direction * PADDLE_SPEED
        self.rect.y = max(WALL_THICKNESS, min(self.rect.y, HEIGHT - WALL_THICKNESS - PADDLE_HEIGHT))

    def draw(self, screen):
        """Draws the paddle on the screen."""
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    """Represents the pong ball."""

    def __init__(self, x, y):
        """Initializes the ball at the given position."""
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y  # Initial vertical speed
        self.ping_sound = pygame.mixer.Sound("ping.ogg")
        self.pong_sound = pygame.mixer.Sound("pong.ogg")

    def move(self, paddle1, paddle2):
        """Moves the ball, handling collisions."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top/bottom walls
        if self.rect.top <= WALL_THICKNESS or self.rect.bottom >= HEIGHT - WALL_THICKNESS:
            self.speed_y *= -1
            self.ping_sound.play()

        # Bounce off paddles (with angle calculation)
        if self.rect.colliderect(paddle1.rect):
            self.handle_paddle_collision(paddle1)
            self.pong_sound.play()
        elif self.rect.colliderect(paddle2.rect):
            self.handle_paddle_collision(paddle2)
            self.pong_sound.play()


    def handle_paddle_collision(self, paddle):
        """Calculates the reflection angle based on the collision point."""
        # Calculate relative collision point (0 at top, 1 at bottom)
        relative_intersect_y = (paddle.rect.centery - self.rect.centery) / (PADDLE_HEIGHT / 2)
        # Clamp the relative intersect Y to be between -1 and 1
        relative_intersect_y = max(-1, min(1, relative_intersect_y))

        # Calculate reflection angle (in radians)
        bounce_angle = relative_intersect_y * math.radians(MAX_REFLECT_ANGLE)

        # Reverse x-direction and set new y-speed based on angle
        self.speed_x *= -1
        self.speed_y = -self.speed_x * math.tan(bounce_angle)  # Use -speed_x for correct reflection
        # Adjust speed based on the bounce angle
        current_speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        
        self.speed_x = math.copysign(current_speed * math.cos(bounce_angle), self.speed_x)
        self.speed_y = -current_speed * math.sin(bounce_angle)


    def draw(self, screen):
        """Draws the ball on the screen."""
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self, direction):
        """Resets the ball."""
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = BALL_SPEED_X * direction
        self.speed_y = BALL_SPEED_Y  # Reset vertical speed as well



class Scoreboard:
    """Manages and displays the game score."""

    def __init__(self):
        """Initializes scores for both players."""
        self.player1_score = 0
        self.player2_score = 0
        self.font = pygame.font.Font(None, FONT_SIZE)

    def update_score(self, ball):
        """Updates the score. Returns True if scored."""
        if ball.rect.left <= 0:
            self.player2_score += 1
            return True
        elif ball.rect.right >= WIDTH:
            self.player1_score += 1
            return True
        return False

    def draw(self, screen):
        """Draws the scoreboard."""
        score_text = f"{self.player1_score} - {self.player2_score}"
        text_surface = self.font.render(score_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 30))
        screen.blit(text_surface, text_rect)

    def check_for_winner(self):
        """Checks for a winner."""
        return self.player1_score >= WINNING_SCORE or self.player2_score >= WINNING_SCORE

    def display_winner(self, screen):
        """Displays the winner."""
        if self.player1_score >= WINNING_SCORE:
            winner_text = "Player 1 Wins!"
        elif self.player2_score >= WINNING_SCORE:
            winner_text = "Player 2 Wins!"
        else:
            return

        font = pygame.font.Font(None, FONT_SIZE * 2)
        text_surface = font.render(winner_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)


class Wall:
    """Represents a wall (top or bottom)."""

    def __init__(self, y, height):
        """Initializes a wall."""
        self.rect = pygame.Rect(0, y, WIDTH, height)

    def draw(self, screen):
        """Draws the wall."""
        pygame.draw.rect(screen, WHITE, self.rect)


class PongGame:
    """Main class for the Pong game."""

    def __init__(self):
        """Initializes game components."""
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        """Resets the game state."""
        self.paddle1 = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.paddle2 = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)
        self.scoreboard = Scoreboard()
        self.game_over = False
        self.ball_direction = 1
        self.top_wall = Wall(0, WALL_THICKNESS)
        self.bottom_wall = Wall(HEIGHT - WALL_THICKNESS, WALL_THICKNESS)

    def handle_input(self):
        """Handles user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle1.move(-1)
        if keys[pygame.K_s]:
            self.paddle1.move(1)
        if keys[pygame.K_UP]:
            self.paddle2.move(-1)
        if keys[pygame.K_DOWN]:
            self.paddle2.move(1)

    def update(self):
        """Updates game state."""
        if not self.game_over:
            self.ball.move(self.paddle1, self.paddle2)
            if self.scoreboard.update_score(self.ball):
                self.ball_direction *= -1
                self.ball.reset(self.ball_direction)
            if self.scoreboard.check_for_winner():
                self.game_over = True

    def draw(self):
        """Draws game elements."""
        self.screen.fill(BLACK)
        self.paddle1.draw(self.screen)
        self.paddle2.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.top_wall.draw(self.screen)
        self.bottom_wall.draw(self.screen)
        if self.game_over:
            self.scoreboard.display_winner(self.screen)
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if not self.game_over:
                self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# --- Main game execution ---
if __name__ == "__main__":
    # Create dummy sound files if they don't exist (for testing)
    if not pygame.mixer.get_init():  # Check if mixer is initialized
      pygame.mixer.init() #mixer needs to be initialized to create sound objects

    try:
        # Attempt to load real sounds
        pygame.mixer.Sound("ping.ogg")
        pygame.mixer.Sound("pong.ogg")
    except pygame.error:
        # If loading fails, create silent placeholder sounds
        print("Sound files not found. Creating silent placeholders.")
        # Create silent placeholder sounds. Use a short sine wave.
        sample_rate = 44100  # Standard sample rate
        duration = 0.1       # 100ms duration
        frequency = 440      # 440 Hz (A4 note)
        # Create an empty array
        silence = pygame.mixer.Sound(buffer=pygame.mixer.Sound(buffer=bytearray(int(sample_rate * duration * 2))).get_raw())

        with open("ping.ogg", "wb") as f:
          f.write(silence.get_raw())
        with open("pong.ogg", "wb") as f:
          f.write(silence.get_raw())


    game = PongGame()
    game.run()