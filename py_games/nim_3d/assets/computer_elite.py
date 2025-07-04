import random
from typing import List, Optional
import assets.strategy as strategy


class ComputerEliteStrategy(strategy.Strategy):
  """An elite robot strategy.

  The robot plays optimally
  """

  def get_turn(self, sticks_remaining: int, max_stick_take: int) -> int:
    if sticks_remaining > max_stick_take:
      take = sticks_remaining % max_stick_take
    else:
      take = sticks_remaining - 1

    # target = 0
    # power_of_2 = 1
    # while power_of_2 - 1 <= sticks_remaining:
    #     target = power_of_2 - 1
    #     power_of_2 *= 2

    # # If the current number of sticks is already a power of 2 minus 1,
    # # any move will lead to a losing position for the current player.
    # # In this case, we just take the maximum allowed.
    # if sticks_remaining == target:
    #     take = min(max_stick_take, sticks_remaining)
    # else:
    #     # Calculate the number of sticks to take to reach the nearest
    #     # power of 2 minus 1.
    #     sticks_to_take = sticks_remaining - target
    #     take = sticks_to_take

    remainder = sticks_remaining % (max_stick_take + 1)

    if remainder == 1:
      # We are in a losing position. Take a random valid number of sticks.
      take = min(max_stick_take, sticks_remaining)
    elif remainder > 1:
      # Take enough sticks to leave a remainder of 1.
      take = remainder - 1
    elif remainder == 0:
      # We are in a winning position. Take the maximum allowed.
      take = min(max_stick_take, sticks_remaining)
    else:
      # This case should ideally not be reached with valid inputs.
      take = 1

    print("computer taking:", take)
    return take
