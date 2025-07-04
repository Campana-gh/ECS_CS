class BasicRobotStrategy():
  """Controls the game based on keyboard input.
  """

  def get_thrust(self, velocity: float, altitude: float, fuel: int) -> bool:
    if velocity > 0.75:
      return True
    else:
      return False
