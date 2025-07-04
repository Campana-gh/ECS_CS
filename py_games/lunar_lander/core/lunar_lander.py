import pygame
import sys
import random
import math
from enum import Enum

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.08  # Adjusted for smoother gameplay
THRUST_POWER = 0.10 # Adjusted for smoother gameplay
INITIAL_FUEL = 225
LANDING_PAD_WIDTH = 100
LANDER_HEIGHT = 60
LANDER_WIDTH = 50
ROCKET_WITH_FLAME_PATH = "assets/rocket_with_flame.png"
ROCKET_WITH_NO_FLAME_PATH = "assets/rocket_with_no_flame.png"
ROCKET_CRASHED_PATH = "assets/rocket_crashed.png"

SAFE_LANDING_SPEED = 1


# Maximum vertical speed for a safe landing
FPS = 60
THRUST_SOUND_PATH = "assets/thruster.wav"
OUT_OF_FUEL_SOUND_PATH = "assets/out_of_fuel.wav"
CRASH_SOUND_PATH = "assets/crash.wav"
VICTORY_SOUND_PATH = "assets/victory.wav"

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)


# --- Classes ---

class RocketImage(Enum):
    WITH_FLAME = 0
    WITH_NO_FLAME = 1
    CRASHED = 2

class LanderSound(Enum):
    NONE = 0
    THRUSTER = 1
    OUT_OF_FUEL = 2
    CRASH = 3
    VICTORY = 4

class Lander:
    """Represents the lunar lander."""

    def __init__(self, screen, x, y, initial_fuel=INITIAL_FUEL):
        """Initializes the lander."""
        self.screen = screen
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.fuel = initial_fuel
        self.crashed = False
        self.landed = False
        self.width = LANDER_WIDTH
        self.height = LANDER_HEIGHT
        self.flame_on = False
        self.sound = LanderSound.NONE
        self.last_sound = LanderSound.NONE
        self.soundboard = {}
        self.soundboard[LanderSound.THRUSTER] = pygame.mixer.Sound(THRUST_SOUND_PATH)
        self.soundboard[LanderSound.OUT_OF_FUEL] = pygame.mixer.Sound(OUT_OF_FUEL_SOUND_PATH)
        self.soundboard[LanderSound.CRASH] = pygame.mixer.Sound(CRASH_SOUND_PATH)
        self.soundboard[LanderSound.VICTORY] = pygame.mixer.Sound(VICTORY_SOUND_PATH)

        self.rocket_images = {}
        self.rocket_images[RocketImage.WITH_FLAME] = pygame.image.load(ROCKET_WITH_FLAME_PATH)
        self.rocket_images[RocketImage.WITH_NO_FLAME] = pygame.image.load(ROCKET_WITH_NO_FLAME_PATH)
        self.rocket_images[RocketImage.CRASHED] = pygame.image.load(ROCKET_CRASHED_PATH)

        for key, value in self.rocket_images.items():
            self.rocket_images[key] = pygame.transform.scale(value, (self.width, self.height))

        self.draw(screen)  # Draw the lander shape onto the surface


    def update(self, thrusting):
        """Updates the lander's position and state."""
        if not self.crashed and not self.landed:
            if thrusting and self.fuel > 0:
                self.velocity_y -= THRUST_POWER
                self.fuel -= 1  # Consume less fuel per frame
                self.flame_on = True
                self.sound = LanderSound.THRUSTER
            else:
                self.flame_on = False
                if self.fuel <= 0:
                    self.sound = LanderSound.OUT_OF_FUEL
                else:
                    self.sound = LanderSound.NONE

            self.velocity_y += GRAVITY
            self.y += self.velocity_y

            # --- Collision Detection ---
            if self.y + self.height >= SCREEN_HEIGHT:  # Ground collision
                # Check for landing or crash
                if self.y + self.height > SCREEN_HEIGHT: #make sure the lander stops *at* the ground
                    self.y = SCREEN_HEIGHT - self.height
                    #self.velocity_y = 0 #ensure that the lander does not go through the floor
                if abs(self.velocity_y) <= SAFE_LANDING_SPEED:
                    self.landed = True
                    self.sound = LanderSound.VICTORY
                else:
                    self.crashed = True

                    self.sound = LanderSound.CRASH
                #self.velocity_y = 0 #Stop on collision, landed or crashed

    def draw(self, screen):
        """Draws the lander on the screen."""
        if self.crashed:
            screen.blit(self.rocket_images[RocketImage.CRASHED], (self.x, self.y))
        elif self.flame_on:
            screen.blit(self.rocket_images[RocketImage.WITH_FLAME], (self.x, self.y))
        else:
            screen.blit(self.rocket_images[RocketImage.WITH_NO_FLAME], (self.x, self.y))

    def play_sound(self):
        """Plays the sound associated with the lander state."""
        if self.sound == self.last_sound:
            return
        if self.last_sound != LanderSound.NONE:
            pygame.mixer.stop()
        if self.sound != LanderSound.NONE:
            if self.sound == LanderSound.THRUSTER:
                loops = -1
            else:
                loops = 0
            self.soundboard[self.sound].play(loops=loops)
        self.last_sound = self.sound


class LandingPad:
    """Represents the landing pad."""
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, 10))

class Game:
    """Manages the game state and logic."""
    def __init__(self, strategy, event_receivers = [], initial_fuel=INITIAL_FUEL):
        """Initializes the game."""
        self.initial_fuel = initial_fuel
        self.event_receivers = event_receivers
        self.strategy = strategy
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mixer.init
        pygame.display.set_caption("Lunar Lander")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        """Resets the game state."""
        #Landing pad
        #self.landing_pad_x = random.randint(0, SCREEN_WIDTH - LANDING_PAD_WIDTH)
        #print(f"Landing pad x: {self.landing_pad_x}")
        self.landing_pad_x = (SCREEN_WIDTH + LANDER_WIDTH - LANDING_PAD_WIDTH) // 2
        self.landing_pad = LandingPad(self.landing_pad_x, SCREEN_HEIGHT - 10, LANDING_PAD_WIDTH)

        #Lander
        self.lander = Lander(self.
                             screen, SCREEN_WIDTH // 2, 50, self.initial_fuel)
        self.lander.landing_pad_x = self.landing_pad_x #Give the lander object access to the landing pad
        self.playing = True

    def run(self):
        """Main game loop."""
        while True:
            thrusting = False #Assume not thrusting unless key is pressed
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

              if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                  self.reset()

            keys = pygame.key.get_pressed()
            for event_receiver in self.event_receivers:
                event_receiver.set_keys(keys)

            if self.playing:
                altitude = (SCREEN_HEIGHT) - self.lander.y - LANDER_HEIGHT
                if self.strategy.get_thrust(self.lander.velocity_y, altitude, self.lander.fuel):
                    thrusting = True
                self.lander.update(thrusting)

            if self.lander.crashed or self.lander.landed:
                self.playing = False

            self.draw()
            self.lander.play_sound()
            self.clock.tick(FPS)

    def draw(self):
        """Draws all game elements."""
        self.screen.fill(BLACK)
        self.lander.draw(self.screen)
        self.landing_pad.draw(self.screen)

        # --- UI Elements ---
        # Fuel Display
        fuel_text = pygame.font.Font(None, 30).render(f"Fuel: {self.lander.fuel:.0f}", True, WHITE)
        self.screen.blit(fuel_text, (10, 10))
        # Vertical velocity
        velocity_text = pygame.font.Font(None, 30).render(f"Speed: {self.lander.velocity_y:.2f}", True, WHITE)
        self.screen.blit(velocity_text, (10, 40))

        # Game Over Message
        if self.lander.crashed:
            game_over_text = pygame.font.Font(None, 50).render("Game Over! You Crashed!", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 4 -50, SCREEN_HEIGHT // 2))
        elif self.lander.landed:
            landing_text = pygame.font.Font(None, 50).render("You Landed Safely!", True, GREEN)
            self.screen.blit(landing_text, (SCREEN_WIDTH // 4 , SCREEN_HEIGHT // 2))

        if not self.playing:
            reset_text = pygame.font.Font(None, 30).render("Press 'R' to restart", True, WHITE)
            self.screen.blit(reset_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

