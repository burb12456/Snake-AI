import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (0, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255)
SNAKE_SPEED = 2  # Adjust this as needed
CHEEDAR = 5
SCORE = 0

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI")

# Snake class
class Snake:
    def __init__(self):
        self.body = [(CHEEDAR, CHEEDAR)]
        self.direction = (0, -1)
        self.grow = False

    def move(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])

        if new_head == food.position:
            self.grow = True

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()

    def change_direction(self, new_direction):
        if new_direction == "UP" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif new_direction == "DOWN" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif new_direction == "LEFT" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif new_direction == "RIGHT" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def check_collision(self):
        if (
            self.body[0] in self.body[1:]
            or self.body[0][0] < 0
            or self.body[0][0] >= GRID_WIDTH
            or self.body[0][1] < 0
            or self.body[0][1] >= GRID_HEIGHT
        ):
            return True
        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def respawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# A* Pathfinding
def find_path(snake, food):
    # If A* fails, just move towards the food
    if snake.body[0][0] < food.position[0]:
        return "RIGHT"
    elif snake.body[0][0] > food.position[0]:
        return "LEFT"
    elif snake.body[0][1] < food.position[1]:
        return "DOWN"
    elif snake.body[0][1] > food.position[1]:
        return "UP"

# Initialize Snake and Food
snake = Snake()
food = Food()

# Main game loop
clock = pygame.time.Clock()
frame_count = 0  # Initialize frame count
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Call your AI logic to determine the next direction for the snake
    if frame_count % SNAKE_SPEED == 0:
        direction = find_path(snake, food)
        snake.change_direction(direction)
        snake.move()

    # Check for collision with food
    if snake.body[0] == food.position:
        snake.grow = False
        SCORE += 1
        food.respawn()

    # Check for collision with walls or itself
    if snake.check_collision():
        pygame.quit()
        sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the snake and food
    snake.draw()
    food.draw()

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(60)  # 60 frames per second
    frame_count += 1
    print("Game loop running")
    print(SCORE)
