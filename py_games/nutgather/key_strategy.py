from typing import List
from core.squirrel_strategy import SquirrelStrategy
from core.position import Position
import pygame

class KeyStrategy(SquirrelStrategy):
  """Represents a squirrel strategy that moves based on key presses."""

  def __init__(self):
    super().__init__()

  def move(self, position: Position, opponent: Position, nuts: List[Position]) -> Position:
    """Moves the squirrel based on key presses."""
    keys = pygame.key.get_pressed()
    x, y = position.x, position.y
    if keys[pygame.K_UP]:
      y -= 1
    if keys[pygame.K_DOWN]:
      y += 1
    if keys[pygame.K_LEFT]:
      x -= 1
    if keys[pygame.K_RIGHT]:
      x += 1

    return Position(x, y)

