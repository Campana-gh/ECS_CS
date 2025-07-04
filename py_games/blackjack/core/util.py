from core.card import Card
from typing import List

def calculate_hand_value(hand:List[Card]) -> int:
  value = sum(card.face_value for card in hand)
  aces = sum(1 for card in hand if card.name == 'A')
  while value > 21 and aces:
    # return the largest hand <= 21 by converting aces to 1.
    value -= 10
    aces -= 1
  return value
  
