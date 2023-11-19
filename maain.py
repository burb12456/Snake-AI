import pygame
import sys
import random
import heapq

POPULATION_SIZE = 50

def initialize_population():
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    population = [random.sample(directions, len(directions)) for _ in range(POPULATION_SIZE)]
    print("Initial population:", population)
    return population

population = initialize_population()

# Initialize Pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Constants
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 50, 255)
SNAKE_SPEED = 10
food_colouring = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
CHEEDAR = 0
temp_count = 0
SCORE = 0
poop = 0
MUTATION_RATE = 0.1
tempScore = 0
CHECK = pygame.time.get_ticks()
timer_start_time = pygame.time.get_ticks()

class Snake:
    def __init__(self):
        initial_x = GRID_WIDTH // 2
        initial_y = GRID_HEIGHT // 2
        self.body = [(initial_x, initial_y)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.grow = False
        self.chromosome = []  # Initialize chromosome here

    def reset_game(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.grow = False

    def move(self, food):
        print("Current direction:", self.direction)
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])

        if new_head == food.position:
            self.grow = True

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()

        if self.check_collision():
            print("Snake direction before dying:", self.direction)

    @staticmethod
    def crossover(parent1, parent2):
        pivot = len(parent1) // 2
        child = parent1[:pivot] + parent2[pivot:]
        return child

    @staticmethod
    def mutate(child):
        for i in range(len(child)):
            if random.random() < MUTATION_RATE:
                child[i] = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        return child

    def change_direction(self, new_direction):
        if new_direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            self.direction = {
                "UP": (0, -1),
                "DOWN": (0, 1),
                "LEFT": (-1, 0),
                "RIGHT": (1, 0)
            }[new_direction]

    def check_collision(self):
        head_x, head_y = self.body[0]

        print("Head position:", head_x, head_y)

        if self.body[0] in self.body[1:]:
            print("Snake collided with itself!")
            return True

        if (
            head_x < 0
            or head_x >= GRID_WIDTH
            or head_y < 0
            or head_y >= GRID_HEIGHT
        ):
            print("Snake went off-screen!")
            return True

        return False

    def draw(self):
        poop = random.randint(0, 150)
        snake_color = (0, poop, 255)
        for segment in self.body:
            pygame.draw.rect(screen, snake_color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


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
        pygame.draw.rect(screen, food_colouring, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def fitness(chromosome, snake, food, elapsed_time):
    growth_reward = snake.grow * 100
    score_reward = SCORE
    time_reward = int(elapsed_time / 1000)
    total_fitness = growth_reward + score_reward + time_reward
    return total_fitness


def move_snake(snake, food):
    print("Entering move_snake")
    print("Snake chromosome:", snake.chromosome)
    if not snake.chromosome:
        snake.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
    else:
        new_direction = snake.chromosome.pop(0)
        snake.change_direction(new_direction)
    snake.move(food)
    print("Exiting move_snake")


def evolve_population(population, snake, food):
    elapsed_time = pygame.time.get_ticks() - CHECK
    parents = heapq.nlargest(int(POPULATION_SIZE * 0.2),
                              population,
                              key=lambda chromosome: fitness(chromosome, snake, food, elapsed_time))
    children = [Snake.crossover(random.choice(parents), random.choice(parents)) for _ in range(POPULATION_SIZE)]
    children = [Snake.mutate(child) for child in children]
    new_population = parents + children
    return new_population


my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT * 1.1))
pygame.display.set_caption("Snake AI")
clock = pygame.time.Clock()


def game_loop():
    global frame_count, temp_count, SCORE, tempScore, population, food_colouring

    frame_count = 0
    snake = Snake()
    food = Food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        move_snake(snake, food)

        if frame_count % SNAKE_SPEED == 0:
            population = evolve_population(population, snake, food)
            elapsed_time = pygame.time.get_ticks() - CHECK
            best_chromosome = max(population, key=lambda chromosome: fitness(chromosome, snake, food, elapsed_time))
            snake.chromosome = best_chromosome.copy()
            move_snake(snake, food)

        if snake.body[0] == food.position:
            snake.grow = False
            SCORE += 1
            food.respawn(snake.body)

        if snake.check_collision():
            pygame.time.delay(100)
            frame_count, temp_count, SCORE, tempScore = 0, 0, 0, 0
            snake.reset_game()

        BLUE = (0, poop, 255)
        screen.fill(WHITE)
        screen.fill(BLACK, (0, 0, GRID_WIDTH * 50, GRID_HEIGHT * 40))
        snake.draw()
        food.draw()

        text_surface = my_font.render("Score: " + str(SCORE), False, (0, 0, 0))
        screen.blit(text_surface, (GRID_WIDTH, GRID_HEIGHT * 41))

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
        temp_count += 1

        if tempScore < SCORE:
            print("Score:", SCORE)
            print("frames per food", temp_count)
            print("Survival Time:", int(elapsed_time / 1000), "seconds")
            temp_count = 0
            food_colouring = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            tempScore = SCORE

    pygame.quit()
    sys.exit()


# Start the game
game_loop()