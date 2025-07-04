import pygame

class KeyStrategy():
  """Controls the game based on keyboard input.
  """

  def __init__(self):
    self.space_pressed = False
        
  def set_keys(self, keys):
    """Sets the key state."""
    if keys[pygame.K_SPACE]:
      self.space_pressed = True
    else:
      self.space_pressed = False

  def get_thrust(self, velocity: float, altitude: float, fuel: int) -> bool:
    """Returns the thrust value based on the key state."""
    if self.space_pressed:
      return True
    else:
      return False
