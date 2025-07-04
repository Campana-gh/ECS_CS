from enum import Enum
import random
import sys
from typing import List
from typing import Optional
import assets.strategy
import pygame

# Initialize Pygame
pygame.init()

# Constants
## Fonts
FONT = pygame.font.Font(None, 36)

## Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Nim")

# Sound Effects
battle_music = pygame.mixer.Sound("assets/battle_music.mp3")
victory_music = pygame.mixer.Sound("assets/victory_music.mp3")
defeat_music = pygame.mixer.Sound("assets/defeat_music.mp3")


## Colors
class Color(Enum):
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  GREEN = (34, 139, 34)
  RED = (255, 0, 0)
  BROWN = (139, 69, 19)
  GRASS = (100, 100, 100)


## Stick properties
STICK_WIDTH = 20
STICK_HEIGHT = 80
STICK_COLOR = Color.BROWN
STICK_SPACING = 30
INITIAL_STICKS = random.randint(20, 30)
MAX_STICK_TAKE = 2

## Button properties
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_COLOR = Color.GRASS
BUTTON_TEXT_COLOR = Color.WHITE
BUTTON_FONT = pygame.font.Font(None, 30)
BUTTON_MARGIN = 10

# End of Constants


class Artist:

  def __init__(self):
    self.decrease_button = None
    self.take_sticks_button = None
    self.increase_button = None
    self.button_reset = None

  def draw_button(
      self, text, x, y, width, height, color: Color, text_color: Color
  ):
    """Draws a button on the screen."""
    pygame.draw.rect(screen, color.value, (x, y, width, height))
    text_surface = BUTTON_FONT.render(text, True, text_color.value)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

  def draw_sticks(self, sticks_left: int):
    """Draws the remaining sticks on the screen."""
    start_x = 10
    y = HEIGHT // 3
    for i in range(sticks_left):
      pygame.draw.rect(
          screen,
          Color.BROWN.value,
          (
              start_x + i * (STICK_WIDTH + STICK_SPACING),
              y,
              STICK_WIDTH,
              STICK_HEIGHT,
          ),
      )

  def display_text(
      self, text, color: Color, x_offset=WIDTH / 2, y_offset=HEIGHT / 2
  ):
    """Displays text on the screen."""
    text_surface = FONT.render(text, True, color.value)
    text_rect = text_surface.get_rect(center=(x_offset, y_offset))
    screen.blit(text_surface, text_rect)

  def draw_game(self, sticks_to_take, sticks_left, text: str = None):
    screen.fill(Color.WHITE.value)
    if text:
      self.display_text(text, Color.BLACK, 400, 150)
    self.display_text("Sticks Left " + str(sticks_left), Color.BLACK, 400, 350)
    self.draw_sticks(sticks_left)
    self.decrease_button = self.draw_button(
        "Decrease",
        WIDTH // 4 - BUTTON_WIDTH // 2,
        HEIGHT * 2 // 3,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        Color.RED,
        BUTTON_TEXT_COLOR,
    )
    self.take_sticks_button = self.draw_button(
        "Take " + str(sticks_to_take),
        WIDTH // 2 - BUTTON_WIDTH // 2,
        HEIGHT * 2 // 3,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        BUTTON_COLOR,
        BUTTON_TEXT_COLOR,
    )
    self.increase_button = self.draw_button(
        "Increase",
        WIDTH * 3 // 4 - BUTTON_WIDTH // 2,
        HEIGHT * 2 // 3,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        Color.GREEN,
        BUTTON_TEXT_COLOR,
    )
    self.button_reset = self.draw_button(
        "Reset",
        WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
        BUTTON_MARGIN,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        BUTTON_COLOR,
        BUTTON_TEXT_COLOR,
    )
    pygame.display.flip()


class Game:

  def __init__(
      self,
      robot_mode: bool,
      player_strategy,
      computer_strategy,
      mouse_receivers,
      delay_seconds=2,
  ):
    # Pygame setup
    self.sticks_left = random.randint(20, 30)
    self.robot_mode = robot_mode
    self.player_strategy = player_strategy
    self.computer_strategy = computer_strategy
    self.mouse_recievers = mouse_receivers
    self.game_over = False
    self.winner_text = ""
    self.delay = delay_seconds * 1000  # Delay in ms
    self.player_turn = True  # random.choice([True, False])  # True for player, False for computer (optional AI)
    self.artist = Artist()
    print(
        "Starting the Game of Nim: "
        + str(self.sticks_left)
        + " with Robot Mode: "
        + str(self.robot_mode)
        + " and Starting with Player: "
        + str(self.player_turn)
    )
    battle_music.play()

  def reset_game(self):
    self.__init__(
        self.robot_mode,
        self.player_strategy,
        self.computer_strategy,
        self.mouse_recievers,
    )

  def check_win(self):
    """Checks if the game is over and determines the winner."""
    if self.sticks_left <= 0:
      self.game_over = True
      if not self.player_turn:
        self.winner_text = "You Win!"
      else:
        self.winner_text = "Computer Wins!"  # If you implement AI

    self.sticks_left = INITIAL_STICKS

  def run(self):
    # Game loop
    running = True
    turn_text = ""
    sticks_to_take = 1
    self.artist.draw_game(sticks_to_take, self.sticks_left)
    display_text = None
    while running:

      # Display current turn
      if not self.game_over:
        display_text = "Your Turn" if self.player_turn else "Computer's Turn"

      if pygame.event.peek():
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
          if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.robot_mode:
              if self.player_turn:
                self.player_strategy.process_mouse(self, event.pos)
                sticks_to_take, turn_over = self.player_strategy.get_turn(
                    self.sticks_left, MAX_STICK_TAKE, sticks_to_take
                )
                if turn_over:
                  self.sticks_left -= sticks_to_take
              else:
                computer_sticks_to_take = self.computer_strategy.get_turn(
                    self.sticks_left, MAX_STICK_TAKE
                )
                self.sticks_left -= computer_sticks_to_take
                turn_over = True

              if turn_over:
                self.player_turn = not self.player_turn

      if self.robot_mode:
        if self.player_turn:
          sticks_to_take = self.player_strategy.get_turn(
              self.sticks_left, MAX_STICK_TAKE
          )
          if sticks_to_take > MAX_STICK_TAKE:
            print(
                "Cheating was detected! Human foolishly tried to take",
                sticks_to_take,
                "when the max they can take is:",
                MAX_STICK_TAKE,
            )
            pygame.quit()
            sys.exit()
        else:
          sticks_to_take = self.computer_strategy.get_turn(
              self.sticks_left, MAX_STICK_TAKE
          )

        self.sticks_left -= sticks_to_take
        self.player_turn = not self.player_turn  # End your turn
        self.artist.draw_game(sticks_to_take, self.sticks_left, display_text)
        print("Sticks left after turn:", self.sticks_left)
        pygame.time.delay(self.delay)  # Sleep a few seconds

      if self.sticks_left <= 0:
        self.game_over = True
        # Display game over message
        if self.player_turn:
          display_text = "Game Over! Humanity is Victorious"
          victory_music.play()
        else:
          display_text = "Game Over! The Robot Overlords Have Prevailed"
          defeat_music.play()

        running = False

      self.artist.draw_game(sticks_to_take, self.sticks_left, display_text)

    pygame.time.delay(20000)  # Pause to let you read the game count
    print(self.winner_text)
    pygame.quit()
    sys.exit()
