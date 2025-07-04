from player_strategy import PlayerStrategy, Movement

class StudentsStrategy(PlayerStrategy):
  """Can you beat me?"""

  def get_move(self, distance_from_last_save: int,  close_to_finish: bool) -> Movement:
    """Get the move for the player.
    
    distance_from_last_save: How far the player has moved since their last save.
    If they get caught by a red light, they will lose this much distance.
    
    close_to_finish: Are we close to the finish. The game selects red light
    more often when we are close to the finish.
    
    Returns:
      Movement.GO -- go forward. Advance 1 step if green light. If red light,
      lose all the way to the last saved point.
      Movement.STOP -- Stop. Save our location in case we get caught by a red
      light.
    """
    # At the start of the game, the probability of a stop is 10%.
    # Close to the finish, the probability of a stop is 40%
    if distance_from_last_save == 0:
      return Movement.GO
    else:
      return Movement.STOP
