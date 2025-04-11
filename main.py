import sys
import pygame
from pygame import Vector2
from random import randint

from settings import *


class Snake:
    def __init__(self):
        self.body = [Vector2(6, 14), Vector2(5, 14), Vector2(4, 14)]
        self.direction = Vector2(0, 0)

    def update(self):
        if self.direction != Vector2(0, 0):
            self.body = self.body[:-1]
            self.body.insert(0, self.body[0] + self.direction)


class Food(pygame.sprite.Sprite):
    def __init__(self, pos, groups: pygame.sprite.AbstractGroup):
        super().__init__(groups)
        self.pos = pos
        self.image = pygame.image.load('images/food.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect(topleft=(self.pos.x * cell_size, self.pos.y * cell_size))

    def update(self):
        pass


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.stroke_panel = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (number_of_cells - 5) * cell_size, (number_of_cells - 5) * cell_size)
        self.stroke_panel.center = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        self.MOVE_SNAKE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_SNAKE, 200)

        self.all_sprites = pygame.sprite.Group()

        self.snake = Snake()
        self.score = 0
        self.food = None

    def draw(self):
        self.screen.fill((171, 200, 95))
        pygame.draw.rect(self.screen, (43, 51, 24), self.stroke_panel, 3)

        for segment in self.snake.body:
            segment_rect = (segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(self.screen, '#4f6015', segment_rect, border_radius=4)

        self.all_sprites.draw(self.screen)

    def check_collision_snake_food(self):
        if self.snake.body[0] == self.food.pos:
            self.food = self.generate_fruit()
            self.snake.body.insert(0, self.snake.body[0] + self.snake.direction)
            self.score += 1
            print(self.score)

    def check_collision_edges(self):
        if self.snake.body[0].x == number_of_cells  or self.snake.body[0].x == -1:
            self.game_over = True
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over = True

    def generate_fruit(self):
        if self.food:
            self.food.kill()
        x, y = (randint(0, number_of_cells - 1),) * 2
        position = Vector2(x, y)

        while position in self.snake.body:
            x, y = (randint(0, number_of_cells - 1),) * 2
            position = Vector2(x, y)

        return Food(position, self.all_sprites)

    def update(self):
        self.draw()
        self.check_collision_snake_food()
        self.all_sprites.update()
        self.check_collision_edges()

    def run(self):

        self.food = self.generate_fruit()
        while self.running:
            for event in pygame.event.get():
                if event.type == self.MOVE_SNAKE and not self.game_over:
                    self.snake.update()
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.snake.direction != [-1, 0]:
                        self.snake.direction = Vector2(1, 0)
                    elif event.key == pygame.K_LEFT and self.snake.direction != [1, 0]:
                        self.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_DOWN and self.snake.direction != [0, -1]:
                        self.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_UP and self.snake.direction != [0, 1]:
                        self.snake.direction = Vector2(0, -1)

            if not self.game_over:
                self.update()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
