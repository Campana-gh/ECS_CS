"""Go-Go-Stop game."""

import dataclasses
import math
import random
from typing import Optional
from daves_strategy import DavesStrategy
from player_strategy import Movement, PlayerStrategy
import pygame
from students_strategy import StudentsStrategy

@dataclasses.dataclass
class Player:
  name: str
  strategy: PlayerStrategy
  color: tuple[int, int, int]
  y_pos: int  # pixel position
  x_pos: int = 0  # pixel position
  saved_step: int = 0  # anchor position
  current_step: int = 0  # current game position
  next_step: int = 0.0  # only used internally while moving
  speed: int = 1  #


# Initialize Pygame
pygame.init()
FONT = pygame.font.SysFont('arial.ttf', 48)

# --- Constants ---
WIDTH, HEIGHT = 800, 200
BOARD_COLOR = (200, 200, 200)  # Light gray
_BLACK = (0, 0, 0)
_PURPLE = (128, 0, 255)
_CYAN = (0, 255, 255)
_GREY = (100, 100, 100)
_GREEN = (0, 255, 0)
_RED = (255, 0, 0)
_WHITE = (255, 255, 255)
STEPS = 32
TOKEN_RADIUS = WIDTH // STEPS // 2
STEP_SIZE = WIDTH // STEPS
FPS = 30  # Frames per second (controls the speed of movement)
_STOP_LIGHT_RADIUS = 24
_STOP_POLYGON = (
    (WIDTH // 2 - _STOP_LIGHT_RADIUS // 2, HEIGHT // 4 - _STOP_LIGHT_RADIUS),
    (WIDTH // 2 + _STOP_LIGHT_RADIUS // 2, HEIGHT // 4 - _STOP_LIGHT_RADIUS),
    (WIDTH // 2 + _STOP_LIGHT_RADIUS, HEIGHT // 4 - _STOP_LIGHT_RADIUS // 2),
    (WIDTH // 2 + _STOP_LIGHT_RADIUS, HEIGHT // 4 + _STOP_LIGHT_RADIUS // 2),
    (WIDTH // 2 + _STOP_LIGHT_RADIUS // 2, HEIGHT // 4 + _STOP_LIGHT_RADIUS),
    (WIDTH // 2 - _STOP_LIGHT_RADIUS // 2, HEIGHT // 4 + _STOP_LIGHT_RADIUS),
    (WIDTH // 2 - _STOP_LIGHT_RADIUS, HEIGHT // 4 + _STOP_LIGHT_RADIUS // 2),
    (WIDTH // 2 - _STOP_LIGHT_RADIUS, HEIGHT // 4 - _STOP_LIGHT_RADIUS // 2),
)
_CLOSED_POLY = 0
_STOP_PROBABILITY = 0.1
_STEPS_CLOSE_TO_FINISH = 12
_STOP_PROBABILITY_NEAR_FINISH = 0.4

# --- Players ---
_players = [
    Player(
        name="Dave",
        strategy=DavesStrategy(),
        y_pos=2 * HEIGHT // 4,
        color=_PURPLE,
    ),
    Player(
        name="Student",
        strategy=StudentsStrategy(),
        y_pos=3 * HEIGHT // 4,
        color=_CYAN,
    ),
]

# --- Game Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reg Light Green Light")
clock = pygame.time.Clock()


def draw_board(is_go: bool, frame_count: int):
  """Draws the board and the tokens."""
  screen.fill(BOARD_COLOR)
  # Draw active (Moving) tokens
  for player in _players:
    pygame.draw.circle(
        screen,
        player.color,
        (player.x_pos + TOKEN_RADIUS, player.y_pos),
        TOKEN_RADIUS,
    )

  # Draw saved (Anchored) tokens
  for player in _players:
    pygame.draw.circle(
        screen,
        player.color,
        (player.saved_step * STEP_SIZE + TOKEN_RADIUS, player.y_pos),
        TOKEN_RADIUS,
        width=4,
    )

  # Draw step markers (optional, for visualization)
  for i in range(STEPS + 1):
    x = i * STEP_SIZE
    pygame.draw.line(screen, _GREY, (x, 0), (x, HEIGHT), 1)

  # Draw the stop / go indicator.
  # TODO(campana):  Add a spinning indicator.
  theta = 2 * math.pi * frame_count / FPS - math.pi / 2
  stop_light_x = WIDTH // 2
  stop_light_y = HEIGHT // 4
  if is_go:
    pygame.draw.circle(
        screen, _GREEN, (stop_light_x, stop_light_y), _STOP_LIGHT_RADIUS
    )
  else:
    pygame.draw.polygon(
        screen, color=_RED, points=_STOP_POLYGON, width=_CLOSED_POLY
    )
  pygame.draw.line(
      screen,
      _BLACK,
      (stop_light_x, stop_light_y),
      (
          stop_light_x + math.cos(theta) * _STOP_LIGHT_RADIUS,
          stop_light_y + math.sin(theta) * _STOP_LIGHT_RADIUS,
      ),
      1,
  )


def animate_players(is_go: bool, game_speed: float = 1.0):
  """Animate the players."""
  # Next, animate the movement.
  frame_count = 0
  while frame_count <= FPS:
    for player in _players:
      # Divide by FPS for smooth movement
      player.x_pos += STEP_SIZE * player.speed / FPS
      # Stop exactly at the end of the move.
      next_pos = player.next_step * STEP_SIZE
      if player.speed > 0:
        if player.x_pos >= next_pos:
          player.x_pos = next_pos
          player.current_step = player.next_step
      else:
        if player.x_pos <= next_pos:
          player.x_pos = next_pos
          player.current_step = player.next_step

    # --- Drawing ---
    draw_board(is_go, frame_count)
    pygame.display.flip()  # Update the display

    # --- Frame Rate Control ---
    clock.tick(FPS * game_speed)
    frame_count += 1


def move_players(is_go: bool, game_speed: float = 1.0) -> bool:
  """Move the players base on their current step"""

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      return True

  # First set next_step as appropriate and then move the players.
  for player in _players:
    if player.speed == 0:
      player.saved_step = player.current_step
      player.next_step = player.saved_step
      continue
    if not is_go:
      # oops, you got caught.
      player.next_step = player.saved_step
      player.speed = -(player.current_step - player.saved_step) * 2
    else:
      player.next_step = player.current_step + player.speed

  animate_players(is_go, game_speed)

  return False


def get_winner() -> Optional[Player]:
  """Returns the name of the player that won (if there is one)."""
  for player in _players:
    if player.x_pos == STEPS * STEP_SIZE:
      return player.name
  return None


def play_game(game_speed: float = 1.0):
  """Plays the game. Main loop."""
  winner = get_winner()
  count = 0
  while not winner:
    distance_from_finish = STEPS - max(
        player.current_step for player in _players
    )
    close_to_finish = distance_from_finish < _STEPS_CLOSE_TO_FINISH
    for player in _players:
      distance_from_last_save = player.current_step - player.saved_step
      move = player.strategy.get_move(distance_from_last_save, close_to_finish)
      if move == Movement.GO:
        player.speed = 1
      else:
        player.speed = 0

    if close_to_finish:
      stop_probability = _STOP_PROBABILITY_NEAR_FINISH
    else:
      stop_probability = _STOP_PROBABILITY
    is_go = False if random.random() < stop_probability else True
    if move_players(is_go, game_speed):
      return
    count += 1
    winner = get_winner()

  if winner == 'Dave':
    color = _PURPLE
  else:
    color = _CYAN
  rendered_text = FONT.render(winner + ' wins!!!', True, color)
  screen.blit(rendered_text, (10, 10))
  pygame.display.flip()
  pygame.time.delay(2000)
