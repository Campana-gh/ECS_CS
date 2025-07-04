from dataclasses import dataclass
from enum import Enum
import math
import random
import sys
from typing import List
from core.position import Position
from core.squirrel_strategy import SquirrelStrategy
from soln.good_robot_strategy import NearestNutStrategy

import pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COUNTDOWN_SIZE = 256
SQUIRREL_SIZE = 48
NUT_SIZE = 24
NUM_NUTS = 30
FONT_SIZE = 36


class Color(Enum):
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  BROWN = (139, 69, 19)
  GRAY = (169, 169, 169)

nut_sound = pygame.mixer.Sound('assets/blue_squirrel.wav')

def move_at_speed(start: Position, dest: Position, speed: float) -> Position:
  """Moves from start to dest at a given speed. Returns the new position."""
  d = SquirrelStrategy.get_distance(start, dest)
  if d < 0.01:
    return dest
  x = start.x + speed * (dest.x - start.x) / d
  y = start.y + speed * (dest.y - start.y) / d
  return Position(x, y)


class GameObject:
  """Base class for game objects."""

  def __init__(self, position: Position, size: int, color: Color, image_path: str):
    self.position = position
    self.size = size
    self.color = color
    self.image = pygame.image.load(image_path)
    self.image = pygame.transform.scale(self.image, (size, size))

    self.rect = pygame.Rect((self.position.x, self.position.y, self.size, self.size))

  def draw(self, screen):
    """Draws the object on the screen."""
    if self.image:
      screen.blit(
          self.image, self.rect.topleft
      )  # Use topleft for blitting images
    else:
      pygame.draw.rect(screen, self.color.value, self.rect)

  def update_rect(self):
    """Keeps rect object updated."""
    self.rect.topleft = (self.position.x, self.position.y)


class Nut(GameObject):
  """Represents a nut."""

  def __init__(self, position: Position, image_path: str):
    super().__init__(position, NUT_SIZE, Color.BROWN.value, image_path)


class NutFarm:
  """Represents all the nuts in the game."""

  def __init__(self, image_path: str):
    self.image_path = image_path
    self.nuts = []

  def get_nuts(self) -> List[Nut]:
    return self.nuts

  def spawn_nuts(self, num_nuts: int, avoid_rects: List[pygame.Rect]):
    """Spawns a nut at a random location, avoiding other objects."""
    while len(self.nuts) < num_nuts:  # Keep trying until we have enough nuts
      x = random.randint(0, SCREEN_WIDTH - NUT_SIZE)
      y = random.randint(0, SCREEN_HEIGHT - NUT_SIZE)
      new_nut = Nut(Position(x, y), self.image_path)
      # Check for collisions with squirrels and existing nuts:
      if all(
          not new_nut.rect.colliderect(rect) for rect in avoid_rects
      ) and all(not new_nut.rect.colliderect(nut.rect) for nut in self.nuts):
        self.nuts.append(new_nut)

  def remove(self, nut: Nut):
    # Remove collected nuts
    self.nuts.remove(nut)


class Squirrel(GameObject):
  """Represents a squirrel."""

  def __init__(
      self,
      position: Position,
      color: Color,
      image_path: str,
      name: str,
      move_strategy: SquirrelStrategy,
  ):
    super().__init__(position, SQUIRREL_SIZE, color, image_path)
    self.speed = 5
    self.score = 0
    self.name = name
    self.move_strategy = move_strategy

  def move(self, opponent: Position, nuts: List[Position]):
    """Moves the squirrel based on key presses."""
    next_target = self.move_strategy.move(self.position, opponent, nuts)
    if not next_target:
      return
    next_position = move_at_speed(self.position, next_target, self.speed)
    x, y = next_position.x, next_position.y

    x = min(max(x, 0), SCREEN_WIDTH - self.size)
    y = min(max(y, 0), SCREEN_HEIGHT - self.size)
    self.position = Position(x, y)

    self.update_rect()

  def collect_nut(self, nut):
    """Checks for collision with a nut and updates the score."""
    if self.rect.colliderect(nut.rect):
      nut_sound.play()
      self.score += 1
      
      return True  # Indicate that the nut was collected
    return False

  def draw_score(self, screen, font, x, y):
    """Draws name and the score"""
    score_text = font.render(
        f"{self.name}: {self.score}", True, self.color.value
    )
    screen.blit(score_text, (x, y))


class Game:
  """Manages the game logic and state."""

  def __init__(self, strategy: SquirrelStrategy):
    self.strategy = strategy
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Squirrel Nut Gathering")
    self.clock = pygame.time.Clock()
    self.font = pygame.font.Font(None, FONT_SIZE)  # Default system font
    self.countdown_font = pygame.font.Font(None, COUNTDOWN_SIZE)
    self.reset()
    self.running = True
    self.count = 0

  def reset(self):
    """Resets the game state for a new game."""
    self.start_time = pygame.time.get_ticks()
    self.nut_farm = NutFarm("assets/nut.png")

    self.red_squirrel = Squirrel(
        Position(50, 50),
        Color.WHITE,
        "assets/red_squirrel.png",
        "Red Squirrel",
        NearestNutStrategy(),
    )
    self.blue_squirrel = Squirrel(
        Position(SCREEN_WIDTH - 50 - SQUIRREL_SIZE, 50),
        Color.GRAY,
        "assets/blue_squirrel.png",
        "Blue Squirrel",
        self.strategy,
    )

    self.nut_farm.spawn_nuts(
        NUM_NUTS, [self.red_squirrel.rect, self.blue_squirrel.rect]
    )
    self.game_over = False

  def handle_input(self):
    """Handles user input events."""
    self.count += 1
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          self.reset()

  def update(self):
    """Updates the game state."""
    if self.game_over:
      return

    self.countdown_timer = (
        3 + (self.start_time - pygame.time.get_ticks()) / 1000
    )
    if self.countdown_timer > 0:
      # nobody can move before the game starts
      return

    # Move the squirrels
    nut_positions = [nut.position for nut in self.nut_farm.get_nuts()]
    self.red_squirrel.move(self.blue_squirrel.position, nut_positions)
    self.blue_squirrel.move(self.red_squirrel.position, nut_positions)

    # Remove collected nuts
    collected_nuts = []
    for nut in self.nut_farm.get_nuts():
      if self.red_squirrel.collect_nut(nut):
        collected_nuts.append(nut)
      elif self.blue_squirrel.collect_nut(nut):
        collected_nuts.append(nut)

    for nut in collected_nuts:
      self.nut_farm.remove(nut)

    # Check for game over
    if not self.nut_farm.get_nuts():
      self.game_over = True

  def draw_countdown(self, screen, font, color: Color):
    """Draws the count down timer."""
    if self.countdown_timer < 0:
      return
    t_displayed = (int)(self.countdown_timer * 10) / 10
    count_down_surface = font.render(str(t_displayed), True, color.value)
    countdown_rect = count_down_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )
    screen.blit(count_down_surface, countdown_rect)

  def draw(self):
    """Renders the game elements on the screen."""
    self.screen.fill(Color.BLACK.value)

    for nut in self.nut_farm.get_nuts():
      nut.draw(self.screen)

    self.red_squirrel.draw(self.screen)
    self.blue_squirrel.draw(self.screen)

    # Display scores
    self.red_squirrel.draw_score(self.screen, self.font, 10, 10)
    self.blue_squirrel.draw_score(
        self.screen, self.font, SCREEN_WIDTH - 250, 10
    )  # Adjust position as needed

    self.draw_countdown(self.screen, self.countdown_font, Color.WHITE)

    if self.game_over:
      self.draw_game_over()

    pygame.display.flip()

  def draw_game_over(self):
    """Displays the game over message and results."""
    if self.red_squirrel.score > self.blue_squirrel.score:
      winner_text = self.red_squirrel.name + " Wins!"
    elif self.blue_squirrel.score > self.red_squirrel.score:
      winner_text = self.blue_squirrel.name + " Wins!"
    else:
      winner_text = "It's a Tie!"

    winner_surface = self.font.render(winner_text, True, Color.WHITE.value)
    winner_rect = winner_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )
    self.screen.blit(winner_surface, winner_rect)
    replay_surface = self.font.render("Press R to Restart", True, Color.WHITE.value)
    replay_rect = replay_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    )
    self.screen.blit(replay_surface, replay_rect)

  def run(self):
    """Main game loop."""
    while self.running:
      self.handle_input()
      self.update()
      self.draw()
      self.clock.tick(60)  # Limit frame rate to 60 FPS

    pygame.quit()
    sys.exit()



