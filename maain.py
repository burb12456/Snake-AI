import pygame
import sys
import random
import heapq

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 900
GRID_SIZE = 50
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255)
DARK_GREEN = (0, 50, 255)
SNAKE_SPEED = 5  # Adjust this as needed
CHEEDAR = 0
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

        # Check if the snake hits the wall, and adjust the direction to prevent that


        if new_head == food.position:
            self.grow = True

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()

    def change_direction(self, new_direction):
        if (
            (new_direction == "UP" and self.direction != (0, 1)) or
            (new_direction == "DOWN" and self.direction != (0, -1)) or
            (new_direction == "LEFT" and self.direction != (1, 0)) or
            (new_direction == "RIGHT" and self.direction != (-1, 0))
        ):
            self.direction = {
                "UP": (0, -1),
                "DOWN": (0, 1),
                "LEFT": (-1, 0),
                "RIGHT": (1, 0)
            }[new_direction]

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

    def respawn(self, snake_body):
        while True:
            new_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if new_position not in snake_body:
                self.position = new_position
                break

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def heuristic(a, b, snake_body, walls1, walls2):
    h = abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    # Penalize squares near the wall
    wall_proximity_penalty = 10
    if (
        a[0] < wall_proximity_penalty
        or a[0] >= (walls1 - wall_proximity_penalty)
        or a[1] < wall_proximity_penalty
        or a[1] >= (walls2 - wall_proximity_penalty)
    ):
        h += wall_proximity_penalty

    # Penalize squares near the snake's body, excluding immediate neighbors
    snake_proximity_penalty = 1
    for segment in snake_body[1:]:
        if abs(a[0] - segment[0]) + abs(a[1] - segment[1]) < snake_proximity_penalty:
            h += snake_proximity_penalty

    return h


def find_path(snake, food):
    graph = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Mark the snake's body as obstacles
    for segment in snake.body:
        graph[segment[1]][segment[0]] = -1

    A_HEIGHT = GRID_HEIGHT
    A_WIDTH = GRID_WIDTH

    open_set = []
    closed_set = set()
    came_from = {}

    start = snake.body[0]
    goal = food.position

    heapq.heappush(open_set, (0, start))

    while open_set:
        current_cost, current_node = heapq.heappop(open_set)

        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()

            if snake.grow:
                snake.grow = False
                return

            next_step = path[0]

            # Check if the next step leads to a collision with the wall
            if (
                next_step[0] < 0
                or next_step[0] >= GRID_WIDTH
                or next_step[1] < 0
                or next_step[1] >= GRID_HEIGHT
            ):
                # Optionally, you can handle this collision differently, like stopping the snake.
                return

            # Check if the next step would trap the head with the tail
            if any(
                (next_step[0] + 1, next_step[1]) == snake.body[i] and
                (next_step[0], next_step[1] + 1) == snake.body[i + 1]
                or
                (next_step[0] - 1, next_step[1]) == snake.body[i] and
                (next_step[0], next_step[1] + 1) == snake.body[i + 1]
                or
                (next_step[0] + 1, next_step[1]) == snake.body[i] and
                (next_step[0], next_step[1] - 1) == snake.body[i + 1]
                or
                (next_step[0] - 1, next_step[1]) == snake.body[i] and
                (next_step[0], next_step[1] - 1) == snake.body[i + 1]
                for i in range(len(snake.body) - 2)
            ):
                # Optionally, you can handle this collision differently.
                return

            snake.direction = tuple(map(lambda x, y: x - y, next_step, snake.body[0]))
            return

        closed_set.add(current_node)

        for neighbor in [(current_node[0] + 1, current_node[1]),
                        (current_node[0] - 1, current_node[1]),
                        (current_node[0], current_node[1] + 1),
                        (current_node[0], current_node[1] - 1)]:
            if (
                0 <= neighbor[0] < GRID_WIDTH
                and 0 <= neighbor[1] < GRID_HEIGHT
                and graph[neighbor[1]][neighbor[0]] != -1
                and neighbor not in closed_set
            ):
                tentative_cost = current_cost + 1
                tentative_heuristic = heuristic(neighbor, goal, snake.body, A_WIDTH, A_HEIGHT)
                total_cost = tentative_cost + tentative_heuristic
                if (
                    (total_cost, neighbor) not in open_set
                    or tentative_cost < graph[neighbor[1]][neighbor[0]]
                ):
                    came_from[neighbor] = current_node
                    graph[neighbor[1]][neighbor[0]] = tentative_cost
                    heapq.heappush(open_set, (total_cost, neighbor))

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
        find_path(snake, food)
        find_path(snake, food)
        snake.move()

    # Check for collision with food
    if snake.body[0] == food.position:
        snake.grow = True
        SCORE += 1
        food.respawn(snake.body)

    # Check for collision with walls or itself
    if snake.check_collision():
        pygame.quit()
        sys.exit()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the snake and food
    snake.draw()
    food.draw()

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(180)  # 60 frames per second
    frame_count += 1
    print("Game loop running")
    print("Score:", SCORE)
