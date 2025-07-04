from player_strategy import PlayerStrategy, Movement

class DavesStrategy(PlayerStrategy):
  """Can you beat me?"""
  
  def get_move(self, distance_from_last_save: int,  close_to_finish: bool) -> Movement:
    """Get the move for the player."""
    if close_to_finish:
      if distance_from_last_save == 0:
        return Movement.GO
      else:
        return Movement.STOP
    else:  # Not close to finish
      if distance_from_last_save < 4:
        return Movement.GO
      else:
        return Movement.STOP
