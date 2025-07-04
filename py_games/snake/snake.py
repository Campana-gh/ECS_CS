from enum import Enum
import random
import time
from typing import List
from typing import Tuple
import pygame

# Initialize Pygame
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10  # Controls the speed of the game
GROWTH_RATE = 1  # segments per second


class Direction(Enum):
  UP = (0, -1)
  DOWN = (0, 1)
  LEFT = (-1, 0)
  RIGHT = (1, 0)


class Color(Enum):
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)
  RED = (255, 0, 0)
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  GRAY = (128, 128, 128)
  YELLOW = (255, 255, 0)

SNAKE_COLOR1 = Color.RED
SNAKE_COLOR2 = Color.BLUE
BACKGROUND_COLOR = Color.BLACK

# --- Functions ---


class SnakeStrategy:

  def get_move(
      self,
      occupied_positions: List[Tuple[int, int]],
      position: Tuple[int, int],
      last_direction: Direction,
  ) -> Direction:
    return last_direction


class ArrowKeyStrategy(SnakeStrategy):
  """A strategy where the arrow keys control the direction."""

  def get_move(
      self,
      occupied_positions: List[Tuple[int, int]],
      position: Tuple[int, int],
      last_direction: Direction,
  ) -> Direction:
    # Snake 2 controls (Arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      return Direction.UP
    elif keys[pygame.K_DOWN]:
      return Direction.DOWN
    elif keys[pygame.K_LEFT]:
      return Direction.LEFT
    elif keys[pygame.K_RIGHT]:
      return Direction.RIGHT
    else:
      return last_direction


class WASDStrategy(SnakeStrategy):
  """A strategy where the arrow keys control the direction."""

  def get_move(
      self,
      occupied_positions: List[Tuple[int, int]],
      position: Tuple[int, int],
      last_direction: Direction,
  ) -> Direction:
    # Snake 2 controls (Arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      return Direction.UP
    elif keys[pygame.K_s]:
      return Direction.DOWN
    elif keys[pygame.K_a]:
      return Direction.LEFT
    elif keys[pygame.K_d]:
      return Direction.RIGHT
    else:
      return last_direction


class Snake:
  """Represents a snake."""

  def __init__(
      self,
      strategy: SnakeStrategy,
      start_position: Tuple[int, int],
      direction: Direction,
      color: Color,
  ):
    self.strategy = strategy
    self.direction = direction
    self.head = start_position
    # self.segments[0] = self.head, self.segments[-1] = tail
    self.segments = [self.head]
    self.color = color

  def check_collision(self, occupied_positions: List[Tuple[int, int]]) -> bool:
    """Checks for collisions between snakes and boundaries."""

    # Check boundary collision
    if not (0 <= self.head[0] < GRID_WIDTH and 0 <= self.head[1] < GRID_HEIGHT):
      return True

    # Check collision with other snakes or self.
    if self.head in occupied_positions:
      return True

    return False

  def move(self, other_snake: List[Tuple[int, int]], grow: bool) -> True:
    """Moves the snake. Returns true if there is a collision."""
    occupied_positions = self.segments + other_snake
    direction = self.strategy.get_move(
        occupied_positions, self.head, self.direction
    )
    self.direction = direction
    self.head = (
        self.head[0] + direction.value[0],
        self.head[1] + direction.value[1],
    )

    if grow:
      self.segments = [self.head] + self.segments
    else:
      for i in range(len(self.segments)-1, 0, -1):
        self.segments[i] = self.segments[i-1]
      self.segments[0] = self.head
    
    # Your own head is exempt.
    occupied_positions = self.segments[1:] + other_snake
    return self.check_collision(occupied_positions)

  def draw(self, screen):
    """Draws a snake on the screen."""
    for segment in self.segments:
      pygame.draw.rect(
          screen,
          self.color.value,
          (
              segment[0] * GRID_SIZE,
              segment[1] * GRID_SIZE,
              GRID_SIZE,
              GRID_SIZE,
          ),
      )


class Game:

  def __init__(self):
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    self.draw_grid()

  def draw_grid(self):
    """Draws the grid lines on the screen."""
    for x in range(0, WIDTH, GRID_SIZE):
      pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
      pygame.draw.line(self.screen, (50, 50, 50), (0, y), (WIDTH, y))
    self.screen.fill(BACKGROUND_COLOR.value)

  def display_winner(self, winner):
    """Displays the winner on the screen."""
    font = pygame.font.Font(None, 50)
    if winner == "snake1":
      text = font.render("Blue Wins!", True, SNAKE_COLOR1.value)
    elif winner == "snake2":
      text = font.render("Red Wins!", True, SNAKE_COLOR2.value)
    else:  # draw
      text = font.render("Draw!", True, (255, 255, 255))

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    self.screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(3)  # Show the message for 3 seconds

  def play(self):
    """Main game function."""
    last_growth_time = time.time()
    game_over = False
    winner = None
    clock = pygame.time.Clock()

    # Initialize snakes
    snake1 = Snake(
        WASDStrategy(),
        (GRID_WIDTH // 8, GRID_HEIGHT // 2),
        Direction.RIGHT,
        Color.RED,
    )
    snake2 = Snake(
        ArrowKeyStrategy(),
        (7 * GRID_WIDTH // 8, GRID_HEIGHT // 2),
        Direction.LEFT,
        Color.BLUE,
    )

    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          game_over = True

      # --- Snake Growth ---
      current_time = time.time()
      if current_time - last_growth_time >= 1 / GROWTH_RATE:
        grow = True
        last_growth_time = current_time
      else:
        grow = False

      # --- Snake Movement ---
      # Snake 1 moves
      if snake1.move(snake2.segments, grow):
        game_over = True
        winner = "snake1"

      # Snake 2 moves
      if snake2.move(snake1.segments, grow):
        game_over = True
        winner = "snake2"

      # --- Drawing ---
      self.draw_grid()
      snake1.draw(self.screen)
      snake2.draw(self.screen)
      pygame.display.flip()

      if winner:
        self.display_winner(winner)
        game_over = True

      clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
  Game().play()
