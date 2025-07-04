from core.squirrel_strategy import SquirrelStrategy
from core.position import Position
from typing import List

class StudentStrategy(SquirrelStrategy):
  """The student's strategy goes here? What is it?"""

  def __init__(self):
    super().__init__()

  def move(self, position: Position, opponent: Position, nuts: List[Position]) -> Position:
    """Moves the squirrel based on the strategy."""
    # Find the nut with the shortest distance
    return nuts[0]
