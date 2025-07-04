import random
from typing import List, Optional
import assets.strategy as strategy


class ComputerAdvancedStrategy(strategy.Strategy):
  """A more advanced robot strategy.

  The robot plays randomly until the final move
  """

  def get_turn(self, sticks_remaining: int, max_stick_take: int) -> int:
    """Returns true if the player should hit."""
    if sticks_remaining > max_stick_take + 1:
      take = random.randint(1, max_stick_take)
    else:
      take = max_stick_take - sticks_remaining + 1

    if take >= 0:
      take = 1

    print("computer taking:", take)
    return take
