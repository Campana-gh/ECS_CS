class SuperRobotStrategy:
  """Controls the game based on keyboard input."""


from core.lunar_lander import GRAVITY
from core.lunar_lander import THRUST_POWER


class SuperRobotStrategy:
  """Newtonian physics based strategy."""

  def __init__(self):
    self.thrust = False

  def get_thrust(self, velocity: float, altitude: float, fuel: int) -> bool:
    if not self.thrust:
      # We haven't turned on our thrusters yet, should we?
      # Solve for d = 1/2 a t^2
      # but with initial velocity v
      # if we fired the thrusters now, how long would it take to get to 0 velocity?
      # velocity = t * acceleration
      t = velocity / (THRUST_POWER - GRAVITY)
      # How far would we go in that period?
      # d = velocity / 2.0 * t
      d = velocity * velocity / (THRUST_POWER - GRAVITY) / 2.0
      if d >= altitude:
        self.thrust = True

    return self.thrust
