from core.squirrel_strategy import SquirrelStrategy
from core.position import Position
from typing import List

class BetterRobotStrategy(SquirrelStrategy):
  """Represents a squirrel strategy that moves to the nearest nut."""

  def __init__(self):
    super().__init__()

  def move(self, position: Position, opponent: Position, nuts: List[Position]) -> Position:
    """Moves the squirrel based on the strategy."""
    # Find the nut with the shortest distance
    opponent_nut = self.get_nearest_nut(opponent, nuts)
    if self.get_distance(opponent, opponent_nut) > self.get_distance(position, opponent_nut):
      # I can get to the opponent nut faster than the opponent
      return opponent_nut
    else:
      # We know we can't beat the opponent to his nut, make sure we aren't going
      # for it.
      trimmed_nuts = [nut for nut in nuts if nut != opponent_nut]
      return self.get_nearest_nut(position, trimmed_nuts)

