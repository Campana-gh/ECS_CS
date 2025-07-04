import math
import random
import pygame

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TRACK_COLOR = GRAY
GRASS_COLOR = GREEN
CAR_COLOR = RED

# --- Track parameters ---
TRACK_CENTER_X = WIDTH // 2
TRACK_CENTER_Y = HEIGHT // 2
TRACK_RADIUS_X = 300
TRACK_RADIUS_Y = 200
TRACK_WIDTH = 50
INNER_TRACK_RADIUS_X = TRACK_RADIUS_X - TRACK_WIDTH
INNER_TRACK_RADIUS_Y = TRACK_RADIUS_Y - TRACK_WIDTH

# --- Car parameters ---
CAR_SIZE = (15, 30)  # Width, Height
MAX_SPEED = 5.0
ACCELERATION = 0.05
BRAKING = 0.1
FRICTION = 0.02
SLIDE_FACTOR = 0.1  # Increased for more noticeable sliding
WALL_BOUNCE_FACTOR = -0.3  # Less bounce
START_ANGLE = 90


class Car:

  def __init__(self, x, y, angle):
    self.x = x
    self.y = y
    self.angle = angle
    self.speed = 0
    self.surface = pygame.Surface(CAR_SIZE, pygame.SRCALPHA)
    self.surface.fill(CAR_COLOR)
    self.original_surface = self.surface
    self.rect = self.surface.get_rect(center=(self.x, self.y))
    self.sliding = False  # Track if the car is currently sliding

  def update(self, accelerate, brake):
    if accelerate:
      self.speed += ACCELERATION
    if brake:
      self.speed -= BRAKING

    self.speed *= 1 - FRICTION
    self.speed = max(0, min(self.speed, MAX_SPEED))

    # --- Steering and Sliding ---
    target_angle = self.calculate_target_angle()
    angle_diff = (target_angle - self.angle) % 360
    if angle_diff > 180:
      angle_diff -= 360

    # Adjust steering based on speed (more sliding at higher speeds)
    steering_sensitivity = 0.1  # Base steering sensitivity
    if self.speed > MAX_SPEED * 0.7:  # Start sliding more at 70% of max speed
      steering_sensitivity = 0.03 + (
          1 - (self.speed / MAX_SPEED)
      )  # Reduce steering, increase slide
      self.sliding = True
    else:
      self.sliding = False

    self.angle += angle_diff * steering_sensitivity

    # Add random slide, scaled by speed
    self.angle += self.speed * SLIDE_FACTOR * (random.uniform(-1, 1))
    self.angle %= 360

    radians = math.radians(self.angle)
    self.x += self.speed * math.cos(radians)
    self.y -= self.speed * math.sin(radians)

    self.check_wall_collision()
    self.surface = pygame.transform.rotate(self.original_surface, self.angle)
    self.rect = self.surface.get_rect(center=(int(self.x), int(self.y)))

  def calculate_target_angle(self):
    dx = TRACK_CENTER_X - self.x
    dy = TRACK_CENTER_Y - self.y
    return math.degrees(math.atan2(-dy, dx)) % 360

  def check_wall_collision(self):
    dx = self.x - TRACK_CENTER_X
    dy = self.y - TRACK_CENTER_Y
    distance_squared = (dx**2) / (TRACK_RADIUS_X**2) + (dy**2) / (
        TRACK_RADIUS_Y**2
    )

    if distance_squared > 1:  # Outside outer edge
      # Calculate normal vector (pointing towards track center)
      normal_angle = self.calculate_target_angle()
      normal_rad = math.radians(normal_angle)

      # Push car back inside, along the normal vector
      overshoot = math.sqrt(dx**2 + dy**2) - self.get_ellipse_radius(
          normal_angle
      )
      self.x -= overshoot * math.cos(normal_rad)
      self.y += overshoot * math.sin(
          normal_rad
      )  # negate y, due to top-left origin

      # Reflect velocity vector across the normal
      dot_product = math.cos(math.radians(self.angle)) * math.cos(
          normal_rad
      ) + math.sin(math.radians(self.angle)) * math.sin(normal_rad)

      reflection_angle = (
          2 * normal_angle - self.angle + 180
      )  # +180 to get the actual reflected angle
      self.angle = reflection_angle % 360

      self.speed *= WALL_BOUNCE_FACTOR

    distance_squared = (dx**2) / (INNER_TRACK_RADIUS_X**2) + (dy**2) / (
        INNER_TRACK_RADIUS_Y**2
    )
    if distance_squared < 1:  # Inside inner edge
      # Calculate normal vector (pointing away from track center)
      normal_angle = (
          self.calculate_target_angle() + 180
      ) % 360  # opposite direction
      normal_rad = math.radians(normal_angle)

      # Push car back inside, along the normal vector
      overshoot = self.get_ellipse_radius(normal_angle, inner=True) - math.sqrt(
          dx**2 + dy**2
      )
      self.x -= overshoot * math.cos(normal_rad)  # +
      self.y += overshoot * math.sin(normal_rad)  # negate y

      # Reflect velocity
      dot_product = math.cos(math.radians(self.angle)) * math.cos(
          normal_rad
      ) + math.sin(math.radians(self.angle)) * math.sin(normal_rad)

      reflection_angle = 2 * normal_angle - self.angle + 180
      self.angle = reflection_angle % 360

      self.speed *= WALL_BOUNCE_FACTOR

  def get_ellipse_radius(self, angle_degrees, inner=False):
    """Calculates the radius of the ellipse at a given angle."""
    angle_radians = math.radians(angle_degrees)
    if not inner:
      a = TRACK_RADIUS_X
      b = TRACK_RADIUS_Y
    else:
      a = INNER_TRACK_RADIUS_X
      b = INNER_TRACK_RADIUS_Y
    return (a * b) / math.sqrt(
        (b * math.cos(angle_radians)) ** 2 + (a * math.sin(angle_radians)) ** 2
    )

  def draw(self, screen):
    screen.blit(self.surface, self.rect)


def draw_track(screen):
  outer_rect = pygame.Rect(0, 0, 2 * TRACK_RADIUS_X, 2 * TRACK_RADIUS_Y)
  outer_rect.center = (TRACK_CENTER_X, TRACK_CENTER_Y)
  pygame.draw.ellipse(screen, TRACK_COLOR, outer_rect)

  inner_rect = pygame.Rect(
      0, 0, 2 * INNER_TRACK_RADIUS_X, 2 * INNER_TRACK_RADIUS_Y
  )
  inner_rect.center = (TRACK_CENTER_X, TRACK_CENTER_Y)
  pygame.draw.ellipse(screen, GRASS_COLOR, inner_rect)


def main():
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Oval Car Racing")
  clock = pygame.time.Clock()

  start_x = TRACK_CENTER_X + TRACK_RADIUS_X - TRACK_WIDTH // 2
  start_y = TRACK_CENTER_Y
  car = Car(start_x, start_y, START_ANGLE)

  running = True
  while running:
    accelerate = False
    brake = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      # Use keydown and keyup to avoid key repeat
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          accelerate = True
        if event.key == pygame.K_DOWN:
          brake = True
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
          accelerate = False
        if event.key == pygame.K_DOWN:
          brake = False

    # --- Handle continuous key presses ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      accelerate = True
    if keys[pygame.K_DOWN]:
      brake = True

    car.update(accelerate, brake)

    screen.fill(GREEN)
    draw_track(screen)
    car.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

  pygame.quit()


if __name__ == "__main__":
  main()
