import pygame
from pygame import Vector2
from random import randint

from settings import *


class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

    def move(self):
        pass

    def update(self):
        pass


class Food(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.AbstractGroup):
        super().__init__(groups)
        self.pos = self.generate_random_pos()
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(self.pos.x * cell_size, self.pos.y * cell_size))

    @staticmethod
    def generate_random_pos():
        x, y = (randint(0, number_of_cells - 1),) * 2
        return Vector2(x, y)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.running = True
        self.stroke_panel = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 500, 500)
        self.stroke_panel.center = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        self.all_sprites = pygame.sprite.Group()

        self.snake = Snake()
        self.food = Food(self.all_sprites)

    def run(self):
        while self.running:
            self.screen.fill((171, 200, 95))
            pygame.draw.rect(self.screen, (43, 51, 24), self.stroke_panel, 3)
            for segment in self.snake.body:
                pass

            self.all_sprites.draw(self.screen)
            self.all_sprites.update()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(10)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
