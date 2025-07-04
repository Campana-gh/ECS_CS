import random
from typing import List, Optional
import assets.strategy as strategy


class ComputerBasicStrategy(strategy.Strategy):
  """A very basic robot strategy.

  The robot plays randomly
  """

  def get_turn(self, sticks_remaining: int, max_stick_take: int) -> int:
    """Returns true if the player should hit."""
    take = random.randint(1, min(sticks_remaining, max_stick_take))
    print("computer taking:", take)
    return take
