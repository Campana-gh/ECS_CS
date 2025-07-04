import pygame
import random
import sys
import math

# --- Constants ---
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)  # Ice color

# Player properties
PLAYER_SIZE = 20
PLAYER_ACCELERATION = 0.3
PLAYER_FRICTION = 0.02  # Simulate ice
MAX_SPEED = 5

# --- Helper Functions ---
def distance(p1, p2):
    """Calculates the distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


# --- Classes ---
class Player(pygame.sprite.Sprite):
    """Represents a player in the game."""

    def __init__(self, x, y, color, is_tagger=False):
        """Initializes a Player object."""
        super().__init__()
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.vx = 0  # Velocity in x direction
        self.vy = 0  # Velocity in y direction
        self.color = color
        self.is_tagger = is_tagger
        self.acceleration = PLAYER_ACCELERATION
        self.friction = PLAYER_FRICTION
        self.max_speed = MAX_SPEED

    def update(self):
        """Updates the player's position and velocity."""

        # Apply friction (ice effect)
        self.vx *= (1 - self.friction)
        self.vy *= (1 - self.friction)

        # Limit speed
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (int(self.x), int(self.y))

        # Keep player within bounds
        self.x = max(PLAYER_SIZE // 2, min(self.x, WIDTH - PLAYER_SIZE // 2))
        self.y = max(PLAYER_SIZE // 2, min(self.y, HEIGHT - PLAYER_SIZE // 2))
        self.rect.center = (int(self.x), int(self.y)) # crucial to update the rect!

    def move(self, dx, dy):
        """Accelerates the player in the given direction."""
        self.vx += dx * self.acceleration
        self.vy += dy * self.acceleration

    def check_tag(self, other):
      """Checks if this player has tagged another player."""
      if self.is_tagger and distance(self.rect.center, other.rect.center) <= PLAYER_SIZE:
          self.is_tagger = False
          other.is_tagger = True
          self.image.fill(self.color)  # Restore original color
          other.image.fill(RED)       # Mark the new tagger
          return True
      return False



class Game:
    """Manages the game logic and state."""

    def __init__(self):
        """Initializes the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ice Tag")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()

        self.player1 = Player(100, 100, BLUE, is_tagger=False)
        self.player2 = Player(700, 500, RED, is_tagger=True)  # Start as tagger

        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        self.running = True
        self.font = pygame.font.Font(None, 36)


    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()



    def handle_events(self):
        """Handles user input and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


        # Player 1 movement (WASD)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player1.move(0, -1)
        if keys[pygame.K_s]:
            self.player1.move(0, 1)
        if keys[pygame.K_a]:
            self.player1.move(-1, 0)
        if keys[pygame.K_d]:
            self.player1.move(1, 0)


        # Player 2 movement (Arrow keys) - only if player2 is the tagger.
        if keys[pygame.K_UP]:
            self.player2.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.player2.move(0, 1)
        if keys[pygame.K_LEFT]:
            self.player2.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.player2.move(1, 0)

    def update(self):
        """Updates game state."""
        self.all_sprites.update()

        # Check for tag
        if self.player2.check_tag(self.player1):
            print("Player 2 tagged Player 1!")  # Debugging
        elif self.player1.check_tag(self.player2):
            print("Player 1 tagged Player 2!")



    def draw(self):
        """Renders the game elements."""
        self.screen.fill(LIGHT_BLUE)  # Ice-like background
        self.all_sprites.draw(self.screen)

        # Display who is the tagger
        if self.player1.is_tagger:
            text = self.font.render("Player 1 is the Tagger", True, BLACK)
        elif self.player2.is_tagger:
            text = self.font.render("Player 2 is the Tagger", True, BLACK)
        else: #should not happen
            text = self.font.render("Nobody is the Tagger??", True, BLACK)

        text_rect = text.get_rect(center=(WIDTH // 2, 20))
        self.screen.blit(text, text_rect)

        pygame.display.flip()



# --- Main Execution ---
if __name__ == "__main__":
    game = Game()
    game.run()