# Simple Snake Game with multiple levels using Pygame
# Run this code with: python main.py

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)


class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.length = 3

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        if new_head in self.positions:
            raise Exception("Game Over")
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def draw(self):
        for pos in self.positions:
            rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)


class Food:
    def __init__(self, snake_positions=None, obstacles=None):
        if snake_positions is None:
            snake_positions = []
        if obstacles is None:
            obstacles = []
        self.position = (0, 0)
        self.respawn(snake_positions, obstacles)

    def respawn(self, snake_positions, obstacles):
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in snake_positions and pos not in obstacles:
                self.position = pos
                break

    def draw(self):
        rect = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect)


class Level:
    """Represents a game level with speed and obstacles."""

    def __init__(self, number, snake_positions):
        self.number = number
        self.speed = 10 + number * 2
        self.obstacles = self._create_obstacles(number - 1, snake_positions)

    def _create_obstacles(self, count, snake_positions):
        obstacles = []
        for _ in range(count):
            while True:
                pos = (
                    random.randint(0, GRID_WIDTH - 1),
                    random.randint(0, GRID_HEIGHT - 1),
                )
                if pos not in snake_positions and pos not in obstacles:
                    obstacles.append(pos)
                    break
        return obstacles

    def draw(self):
        for pos in self.obstacles:
            rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, rect)


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLUE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLUE, (0, y), (WIDTH, y))


def show_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def main():
    snake = Snake()
    level_num = 1
    level = Level(level_num, snake.positions)
    food = Food(snake.positions, level.obstacles)
    score = 0
    running = True

    while running:
        clock.tick(level.speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(1, 0)

        try:
            snake.move()
        except Exception:
            running = False

        if snake.positions[0] in level.obstacles:
            running = False

        if snake.positions[0] == food.position:
            snake.length += 1
            score += 1
            if score % 5 == 0:
                level_num += 1
                level = Level(level_num, snake.positions)
            food.respawn(snake.positions, level.obstacles)

        screen.fill(BLACK)
        draw_grid()
        level.draw()
        snake.draw()
        food.draw()
        show_text(f'Score: {score}  Level: {level_num}', WHITE, 10, 10)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
