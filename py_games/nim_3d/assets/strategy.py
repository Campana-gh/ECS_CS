from core.nim_game import Game
import pygame


class MouseReceiver:
  """Only used by classes that need to receive keys."""

  def process_mouse(self, game: Game, mouse_loc) -> None:
    # print("Default Process Mouse")
    pass


class Strategy:

  def get_turn(self, sticks_remaining: int, max_stick_take: int) -> int:
    # print ("Default Get Turn Funct")
    return 1
