import random
from typing import List, Optional, Tuple
import assets.strategy as strategy


class HumanStrategy(strategy.Strategy):
  """An elite robot strategy.

  The robot plays optimally
  """

  def get_turn(self, sticks_remaining: int, max_stick_take: int) -> int:
    ##############################################################################
    # Add your logic here
    # You must return a Tuple(num_sticks_you_want_to_take, True /* You wish to end your turn */)
    amount_to_take = 2
    print("Human is taking", amount_to_take)
    return amount_to_take
    ##############################################################################
