from typing import List, Optional
import player_strategy
from core.card import Card
from player_strategy import HitOrStay


class BasicRobotStrategy(player_strategy.PlayerStrategy):
  """A very basic robot strategy.
  """

  def get_hit(self, player_hand: List[Card], dealer_card: Card) -> Optional[HitOrStay]:
    """Returns HitOrStay.STAY or HitOrStay.HIT."""
    # Always return STAY. You will lose a lot of games this way :-)
    return HitOrStay.STAY

  def is_human(self) -> bool:
    """Controls whether we need to pause and play sounds."""
    return False
