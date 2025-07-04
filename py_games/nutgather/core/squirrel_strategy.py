from typing import List
from core.position import Position
import math


class SquirrelStrategy:
  """Represents a squirrel strategy."""

  # --- Helper Functions ---
  @staticmethod
  def get_distance(p1: Position, p2: Position) -> float:
    """Calculates the Euclidean distance between two positions."""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

  @staticmethod
  def get_nearest_nut(position: Position, nuts: List[Position]) -> Position:
    """Returns closest nut to the given position."""
    min_distance = None
    min_nut = None
    for nut in nuts:
      distance = SquirrelStrategy.get_distance(position, nut)
      if not min_distance or distance < min_distance:
        min_distance = distance
        min_nut = nut
    return min_nut
  
  def move(self, position: Position, opponent: Position, nuts: List[Position]) -> Position:
    """Moves the squirrel based on the strategy.
    position is the current position of the squirrel. Returns the target location
    to move to.
    """
    pass