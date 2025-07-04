import pygame
import random
import copy

# --- Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_LEFT = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_TOP = SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE
FPS = 30  # Frames per second
FALL_SPEED = 0.8  # Initial falling speed (seconds per block)
FAST_FALL_SPEED = 0.08 #seconds per block when down key is pressed

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# --- Shapes ---
SHAPES = [
    [[1, 1, 1, 1]],  # I-piece
    [[1, 0, 0], [1, 1, 1]],  # J-piece
    [[0, 0, 1], [1, 1, 1]],  # L-piece
    [[0, 1, 1], [1, 1, 0]],  # S-piece
    [[1, 1, 0], [0, 1, 1]],  # Z-piece
    [[1, 1], [1, 1]],       # O-piece
    [[0, 1, 0], [1, 1, 1]]   # T-piece
]
SHAPE_COLORS = [CYAN, BLUE, ORANGE, GREEN, RED, YELLOW, MAGENTA]


class Piece:
    """Represents a Tetris piece (Tetromino)."""

    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0  # Current rotation state

    def rotate(self):
        """Rotates the piece clockwise."""
        self.rotation = (self.rotation + 1) % 4  # Cycle through rotations
        self.shape = self._rotate_shape()

    def _rotate_shape(self):
      """Rotates the current shape 90 degrees clockwise.
          Uses a list comprehension for conciseness."""
      rows = len(self.shape)
      cols = len(self.shape[0])

      # Transpose and reverse rows to rotate
      new_shape = [[self.shape[j][i] for j in range(rows - 1, -1, -1)] for i in range(cols)]
      return new_shape

    def get_positions(self):
        """Returns a list of (x, y) positions occupied by the piece."""
        positions = []
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    positions.append((self.x + j, self.y + i))
        return positions

class Grid:
    """Represents the Tetris game grid."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[(0, BLACK) for _ in range(width)] for _ in range(height)]  # (filled, color)

    def is_valid_position(self, piece):
        """Checks if the piece's position is valid (within bounds and not colliding)."""
        for x, y in piece.get_positions():
            if x < 0 or x >= self.width or y >= self.height or (y >= 0 and self.grid[y][x][0] == 1):
                return False  # Out of bounds or collision
        return True

    def lock_piece(self, piece):
        """Locks the piece into the grid."""
        for x, y in piece.get_positions():
            if y >= 0:  # Important: Prevent indexing errors for pieces partially above the grid
              self.grid[y][x] = (1, piece.color)

    def clear_rows(self):
        """Clears completed rows and returns the number of rows cleared."""
        rows_cleared = 0
        new_grid = []
        for row in self.grid:
          if all(cell[0] == 1 for cell in row): #If all blocks in row are full
            rows_cleared += 1 #increment completed rows
          else:
            new_grid.append(row)
        
        #add empty rows to the top
        for _ in range(rows_cleared):
          new_grid.insert(0,[(0,BLACK) for _ in range(self.width)])

        self.grid = new_grid
        return rows_cleared
    
    def is_game_over(self):
      """Check for game over condition."""
      for cell in self.grid[0]:
        if cell[0] == 1:
          return True
      return False

    def draw(self, surface):
        """Draws the grid on the given surface."""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell[0] == 1:
                    pygame.draw.rect(surface, cell[1],
                                     (GRID_LEFT + x * BLOCK_SIZE, GRID_TOP + y * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)
                # Draw grid lines
                pygame.draw.rect(surface, GRAY,
                                 (GRID_LEFT + x * BLOCK_SIZE, GRID_TOP + y * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 1)


class TetrisGame:
    """Manages the overall Tetris game logic."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.fall_time = 0  # Accumulated time for falling
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)  # Default font, size 36


    def new_piece(self):
        """Creates a new random piece."""
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        return Piece(GRID_WIDTH // 2 - 2, -2, shape, color)

    def handle_input(self):
        """Handles user input (key presses)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_piece(-1, 0)  # Move left
                if event.key == pygame.K_RIGHT:
                    self.move_piece(1, 0)   # Move right
                if event.key == pygame.K_DOWN:
                  self.move_piece(0,1,fast_fall=True)   # Move down faster
                if event.key == pygame.K_UP:
                    self.rotate_piece()    # Rotate

    def move_piece(self, dx, dy, fast_fall=False):
        """Moves the current piece by (dx, dy) if the move is valid."""
        temp_piece = copy.deepcopy(self.current_piece)  # Work on a copy
        temp_piece.x += dx
        temp_piece.y += dy

        if self.grid.is_valid_position(temp_piece):
            self.current_piece.x += dx
            self.current_piece.y += dy
            if fast_fall:
                self.fall_time += FALL_SPEED-FAST_FALL_SPEED #makes piece fall more natural, accounts for extra time taken
            return True # Moved Successfully
        return False

    def rotate_piece(self):
      """Rotates the current piece, handling potential wall kicks."""
      original_x = self.current_piece.x # Store original position
      original_y = self.current_piece.y
      temp_piece = copy.deepcopy(self.current_piece) # Create a deep copy
      temp_piece.rotate() # Rotate the copy

      if self.grid.is_valid_position(temp_piece):
        self.current_piece.rotate()
        return # Rotation successful

      # Wall kick attempts (check offsets if the rotation caused a collision)
      offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1), (0, 1), (-1, 1),(1,1)]

      for offset_x, offset_y in offsets:
          temp_piece.x = original_x + offset_x
          temp_piece.y = original_y + offset_y
          if self.grid.is_valid_position(temp_piece): # Check with updated position
              self.current_piece.x = temp_piece.x   # Apply the successful offset
              self.current_piece.y = temp_piece.y
              self.current_piece.shape = temp_piece.shape
              self.current_piece.rotation = temp_piece.rotation
              return  # Wall kick successful
      # No valid rotation or wall kick found.  Piece stays as it was.


    def update(self, dt):
      """Updates the game state (piece falling, clearing rows, etc.)."""
      if self.game_over:
          return
      
      self.fall_time += dt
      if self.fall_time >= FALL_SPEED:
        self.fall_time = 0
        if not self.move_piece(0, 1):  # Try to move down. If it fails...
          self.grid.lock_piece(self.current_piece)
          rows_cleared = self.grid.clear_rows()
          self.score += rows_cleared * 100  # Example scoring
          self.current_piece = self.next_piece
          self.next_piece = self.new_piece()
          if not self.grid.is_valid_position(self.current_piece):
            self.game_over = True

      if self.grid.is_game_over():
        self.game_over = True
        

    def draw(self):
        """Draws the game elements (grid, pieces, score, etc.)."""
        self.screen.fill(BLACK)
        self.grid.draw(self.screen)

        # Draw current piece
        for x, y in self.current_piece.get_positions():
            pygame.draw.rect(self.screen, self.current_piece.color,
                             (GRID_LEFT + x * BLOCK_SIZE, GRID_TOP + y * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE), 0)
        
        # Draw next piece
        next_piece_x_offset = GRID_LEFT + GRID_WIDTH * BLOCK_SIZE + 50  # Example offset
        next_piece_y_offset = GRID_TOP + 50
        for i, row in enumerate(self.next_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                  pygame.draw.rect(
                      self.screen,
                      self.next_piece.color,
                      (
                          next_piece_x_offset + j * BLOCK_SIZE,
                          next_piece_y_offset + i * BLOCK_SIZE,
                          BLOCK_SIZE,
                          BLOCK_SIZE,
                      ),
                      0,
                  )

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))  # Position the score text

        if self.game_over:
          game_over_text = self.font.render("Game Over", True, RED)
          text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
          self.screen.blit(game_over_text, text_rect) # Center the text

        pygame.display.flip()


    def run(self):
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            self.handle_input()
            self.update(dt)
            self.draw()

            if self.game_over:
                # Optional: Add a delay before closing, or a "Play Again" option
                pygame.time.delay(2000)  # Wait 2 seconds
                running = False


        pygame.quit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()