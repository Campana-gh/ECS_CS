from typing import List, Optional
from player_strategy import HitOrStay, PlayerStrategy
from core.card import Card


class BetterRobotStrategy(PlayerStrategy):
  """A strategy where the player presses 's' to stand and 'h' to hit."""

  @staticmethod
  def calculate_hand_value(hand: List[Card]) -> int:
    return PlayerStrategy.calculate_hand_value(hand)
    
  def get_hit(self, player_hand: List[Card], dealer_card: Card) -> Optional[HitOrStay]:
    """Returns HitOrStay.STAY or HitOrStay.HIT."""

    # If the player has a hand value of 17 or less, hit.
    if self.calculate_hand_value(player_hand) >= 17:
      return HitOrStay.STAY
    elif self.calculate_hand_value(player_hand) == 16 and dealer_card.face_value in (4,5,6):
      return HitOrStay.STAY
    else:
      return HitOrStay.HIT

  def is_human(self) -> bool:
    """Controls whether we need to pause and play sounds."""
    return False
