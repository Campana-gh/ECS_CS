from typing import List, Optional
import pygame
from core.card import Card
from enum import Enum


class HitOrStay(Enum):
  HIT = 1
  STAY = 2


class KeyReceiver:
  """Only used by classes that need to receive keys."""

  def set_key(self, key: int) -> None:
    pass


class PlayerStrategy:

  @staticmethod
  def calculate_hand_value(hand: List[Card]) -> int:
    value = sum(card.face_value for card in hand)
    aces = sum(1 for card in hand if card.name == 'A')
    while value > 21 and aces:
      # return the largest hand <= 21 by converting aces to 1.
      value -= 10
      aces -= 1
    return value

  def get_hit(self, player_hand: List[Card], dealer_card: Card) -> Optional[HitOrStay]:
    """Returns true if the player should hit.

    cards are of the form '2', '3', ... 'K', 'A'
    """
    return HitOrStay.STAY

  def is_human(self) -> bool:
    """Controls whether we need to pause and play sounds."""
    return False
