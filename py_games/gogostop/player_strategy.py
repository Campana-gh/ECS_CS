from enum import Enum

class Movement(Enum):
    STOP = 0
    GO = 1

class PlayerStrategy:
  """A player strategy."""

  def get_move(self, distance_from_last_save: int, close_to_finish: bool) -> Movement:
      """Get the move for the player."""
      # At the start of the game, the probability of a stop is 10%.
      # Close to the finish, the probability of a stop is 40%
      return Movement.STOP