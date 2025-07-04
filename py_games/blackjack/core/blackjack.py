import dataclasses
from enum import Enum
import random
from typing import List, Tuple
from core.util import calculate_hand_value
from core.card import Card, create_deck, Suit
import player_strategy
import pygame
from player_strategy import HitOrStay

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FONT = pygame.font.SysFont('arial.ttf', 64)

CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_TEXT_OFFSET = (35, 15)
CARD_PIP_OFFSET = (25, 65)
PIP_HEIGHT = 60
PIP_WIDTH = 50
WIN_LOSE_HEIGHT = 200
WIN_LOSE_WIDTH = 200
WIN_LOSE_POS = (500, 20)
CARD_SPACING = 10
COIN_TEXT_POS = (20, 20)
DEALER_HAND_TEXT_POS = (20, 100)
DEALER_HAND_CARDS_POS = (20, 150)
PLAYER_HAND_TEXT_POS = (20, 350)
PLAYER_HAND_CARDS_POS = (20, 400)

blank_card = pygame.transform.scale(
    pygame.image.load('assets/blank_card.png'), (CARD_WIDTH, CARD_HEIGHT)
)
face_down_card = pygame.transform.scale(
    pygame.image.load('assets/face_down_v2.png'), (CARD_WIDTH, CARD_HEIGHT)
)
heart_pip = pygame.transform.scale(
    pygame.image.load('assets/heart_pip.png'), (PIP_WIDTH, PIP_HEIGHT)
)
diamond_pip = pygame.transform.scale(
    pygame.image.load('assets/diamond_pip.png'), (PIP_WIDTH, PIP_HEIGHT)
)
club_pip = pygame.transform.scale(
    pygame.image.load('assets/club_pip.png'), (PIP_WIDTH, PIP_HEIGHT)
)
spade_pip = pygame.transform.scale(
    pygame.image.load('assets/spade_pip.png'), (PIP_WIDTH, PIP_HEIGHT)
)

happy_face = pygame.transform.scale(
    pygame.image.load('assets/happy_gold_with_sunglasses.png'), (WIN_LOSE_WIDTH, WIN_LOSE_HEIGHT)
)
sad_face = pygame.transform.scale(
    pygame.image.load('assets/sad.png'), (WIN_LOSE_WIDTH, WIN_LOSE_HEIGHT)
)
tie_face = pygame.transform.scale(
    pygame.image.load('assets/tie.png'), (WIN_LOSE_WIDTH, WIN_LOSE_HEIGHT)
)

win_sound = pygame.mixer.Sound('assets/win.wav')
tie_sound = pygame.mixer.Sound('assets/tie.wav')
lose_sound = pygame.mixer.Sound('assets/lose.wav')

class Color(Enum):
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  GREEN = (34, 139, 34)
  RED = (255, 0, 0)

@dataclasses.dataclass
class DisplayedSuit:
  image: pygame.Surface
  color: Color

DISPLAYED_SUITS_MAP = {
    Suit.HEARTS: DisplayedSuit(heart_pip, Color.RED),
    Suit.DIAMONDS: DisplayedSuit(diamond_pip, Color.RED),
    Suit.CLUBS: DisplayedSuit(club_pip, Color.BLACK),
    Suit.SPADES: DisplayedSuit(spade_pip, Color.BLACK),
}

class Turn(Enum):
  PLAYER = 1
  DEALER = 2


class Game():
  def __init__(self, strategy: player_strategy.PlayerStrategy, key_receivers: List[player_strategy.KeyReceiver] = []):
    # Pygame setup
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Blackjack')
    self.clock = pygame.time.Clock()
    self.strategy = strategy
    self.key_receivers = key_receivers


  def draw_text(self, text, position, color: Color = Color.WHITE):
    rendered_text = FONT.render(text, True, color.value)
    self.screen.blit(rendered_text, position)


  def render_cards(self, cards: List[Card], position: Tuple[int, int], dealer_hand_turn_hidden: bool = False):
    x, y = position[0], position[1]
    for card in cards:
      self.screen.blit(blank_card, (x, y))
      displayed_suit = DISPLAYED_SUITS_MAP[card.suit]
      rendered_card = FONT.render(card.name, True, displayed_suit.color.value)
      self.screen.blit(rendered_card, (x + CARD_TEXT_OFFSET[0], y + CARD_TEXT_OFFSET[1]))
      displayed_suit = DISPLAYED_SUITS_MAP[card.suit]
      self.screen.blit(displayed_suit.image, (x + CARD_PIP_OFFSET[0], y + CARD_PIP_OFFSET[1]))
      x += CARD_WIDTH + CARD_SPACING
      if dealer_hand_turn_hidden:
        # draw the face down card and stop.
        self.screen.blit(face_down_card, (x, y))
        break


  def render_game(self,
      coins: int,
      games: int,
      player_hand: List[Card],
      dealer_hand: List[Card],
      dealer_hand_turn_hidden: bool,
      emoji: pygame.Surface = None,
  ) -> None:
    self.screen.fill(Color.GREEN.value)
    self.draw_text(f'Coins: {coins}, Games: {games}', COIN_TEXT_POS)
    self.draw_text(f'Dealer Hand:', DEALER_HAND_TEXT_POS)
    self.render_cards(dealer_hand, DEALER_HAND_CARDS_POS, dealer_hand_turn_hidden)
    self.draw_text(f'Player Hand', PLAYER_HAND_TEXT_POS)
    self.render_cards(player_hand, PLAYER_HAND_CARDS_POS)
    if emoji:
      self.screen.blit(emoji, (WIN_LOSE_POS))

    pygame.display.flip()


  def play(self):
    coins = 100
    game_count = 0

    while coins > 0:
      deck = create_deck()

      player_hand = [deck.pop(), deck.pop()]
      dealer_hand = [deck.pop(), deck.pop()]
      dealer_hand_turn_hidden = True
      turn = Turn.PLAYER
      winner = None

      self.render_game(
          coins, game_count, player_hand, dealer_hand, dealer_hand_turn_hidden
      )

      # Player goes first until the bust or hold.
      while turn == Turn.PLAYER and winner is None:
        if pygame.event.peek():
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
              return
            if event.type == pygame.KEYDOWN:
              for key_receiver in self.key_receivers:
                key_receiver.set_key(event.key)
        hit_or_stay = self.strategy.get_hit(player_hand, dealer_hand[0])
        if hit_or_stay == HitOrStay.HIT:
          player_hand.append(deck.pop())
          if calculate_hand_value(player_hand) > 21:
            winner = Turn.DEALER
        elif hit_or_stay == HitOrStay.STAY:
          turn = Turn.DEALER

        self.render_game(
            coins, game_count, player_hand, dealer_hand, dealer_hand_turn_hidden
        )


      # If the player hasn't already busted, the dealer hits until 17.
      if winner is None:
        dealer_hand_turn_hidden = False
        while calculate_hand_value(dealer_hand) < 17:
          dealer_hand.append(deck.pop())
          self.render_game(
              coins, game_count, player_hand, dealer_hand, dealer_hand_turn_hidden
          )

        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if dealer_value > 21 or player_value > dealer_value:
          winner = Turn.PLAYER
        elif player_value < dealer_value:
          winner = Turn.DEALER

      game_count += 1

  
      if winner == Turn.PLAYER:
        emoji = happy_face
        sound = win_sound
        coins += 1
      elif winner == Turn.DEALER:
        emoji = sad_face
        sound = lose_sound
        coins -= 1
      else:
        emoji = tie_face
        sound = tie_sound

      self.render_game(
          coins,
          game_count,
          player_hand,
          dealer_hand,
          dealer_hand_turn_hidden,
          emoji,
      )
 
      if self.strategy.is_human():
        sound.play()
        pygame.time.delay(2000)  # Pause before next round

    pygame.time.delay(4000)  # Pause to let you read the game count
