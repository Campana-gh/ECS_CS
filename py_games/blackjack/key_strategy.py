from typing import List, Optional
import player_strategy
import pygame
from core.card import Card
from player_strategy import HitOrStay


class KeyStrategy(player_strategy.PlayerStrategy, player_strategy.KeyReceiver):
  """A strategy where the player presses 's' to stand and 'h' to hit."""

  def __init__(self):
    self.key = None

  def set_key(self, key: int) -> None:
    self.key = key

  def get_hit(self, player_hand: List[Card], dealer_card: Card) -> Optional[HitOrStay]:
    """Returns HitOrStay.STAY or HitOrStay.HIT."""
    if self.key == pygame.K_h:
      hit = HitOrStay.HIT
    elif self.key == pygame.K_s:
      hit = HitOrStay.STAY
    else:
      hit = None
    self.key = None
    return hit

  def is_human(self) -> bool:
    """Controls whether we need to pause and play sounds."""
    return True
