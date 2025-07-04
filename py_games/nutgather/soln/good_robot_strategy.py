from core.squirrel_strategy import SquirrelStrategy
from core.position import Position
from typing import List

class NearestNutStrategy(SquirrelStrategy):
  """Represents a squirrel strategy that moves to the nearest nut."""

  def __init__(self):
    super().__init__()

  def move(self, position: Position, opponent: Position, nuts: List[Position]) -> Position:
    """Moves the squirrel based on the strategy."""
    # Find the nut with the shortest distance
    move_postion = self.get_nearest_nut(position, nuts)
    return move_postion
