# Card values and deck setup
import dataclasses
from enum import Enum
from typing import List
import random

CARD_VALUES = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11,  # remember, aces can also be 1 :-)
}

# Card values and deck setup
class Suit(Enum):
  HEARTS = 1
  DIAMONDS = 2
  CLUBS = 3
  SPADES = 4

@dataclasses.dataclass
class Card:
  name: str
  face_value: int
  suit: Suit
  
def create_deck() -> List[Card]:
  deck = []
  for suit in Suit:
    for name, face_value in CARD_VALUES.items():
      deck.append(Card(name, face_value, suit))
  random.shuffle(deck)
  return deck