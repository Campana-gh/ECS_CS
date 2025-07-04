from typing import List, Optional
import player_strategy
from core.card import Card
from player_strategy import HitOrStay, PlayerStrategy


class StudentStrategy(PlayerStrategy):
  """A student strategy.
  """
  @staticmethod
  def calculate_hand_value(hand: List[Card]) -> int:
    """Returns the hand value. Counts aces as high unless the hand is 21 or more, then aces are counted as low."""
    return PlayerStrategy.calculate_hand_value(hand)

  def get_hit(self, player_hand: List[Card], dealer_card: Card) -> Optional[HitOrStay]:
    """Returns HitOrStay.STAY or HitOrStay.HIT."""
    # Always return STAY. You will lose a lot of games this way :-)
    return HitOrStay.STAY

  def is_human(self) -> bool:
    """Controls whether we need to pause and play sounds."""
    return False