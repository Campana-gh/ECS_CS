from enum import Enum
import random
from typing import List, Optional, Tuple
import assets.strategy as strategy
import core.nim_game
from core.nim_game import Artist, Game
from core.nim_game import BUTTON_COLOR, BUTTON_HEIGHT, BUTTON_MARGIN, BUTTON_TEXT_COLOR, BUTTON_WIDTH, MAX_STICK_TAKE


class ButtonType(Enum):
  NO_ACTION = 0
  DECREASE = 1
  TAKE_STICKS = 2
  INCREASE = 3
  RESET = 4


class ButtonStrategy(strategy.Strategy, Artist, strategy.MouseReceiver):
  """An elite robot strategy.

  The robot plays optimally
  """

  def __init__(self):
    self.button: ButtonType = None

  def process_mouse(self, game: Game, mouse_loc):
    # print("Processing Mouse Button Action: " + str(mouse_loc) )
    if game.artist.decrease_button.collidepoint(mouse_loc):
      # print("Processing Decrease Action")
      self.button = ButtonType.DECREASE
    elif game.artist.take_sticks_button.collidepoint(mouse_loc):
      self.button = ButtonType.TAKE_STICKS
    elif game.artist.increase_button.collidepoint(mouse_loc):
      self.button = ButtonType.INCREASE
    elif game.artist.button_reset.collidepoint(mouse_loc):
      self.button = ButtonType.RESET

  def get_turn(
      self, sticks_remaining: int, max_stick_take: int, sticks_to_take: int
  ) -> Tuple[int, bool]:
    ##############################################################################
    # Add your logic here
    ret_val = None, None
    if self.button == ButtonType.INCREASE:
      if sticks_to_take < min(sticks_remaining, max_stick_take):
        sticks_to_take += 1
      ret_val = sticks_to_take, False
    elif self.button == ButtonType.DECREASE:
      if sticks_to_take > 1:
        sticks_to_take -= 1
      ret_val = sticks_to_take, False
    elif self.button == ButtonType.TAKE_STICKS:
      print("player taking:", sticks_to_take)
      ret_val = sticks_to_take, True
    elif self.button == ButtonType.RESET:
      ret_val = None, None
    else:
      ret_val = sticks_to_take, False

    self.button = ButtonType.NO_ACTION
    return ret_val
    ##############################################################################
