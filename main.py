import sys
import pygame
from pygame import Vector2
from random import randint

from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, size, text, font, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill((171, 200, 95))
        self.rect = self.image.get_rect(center=pos)
        self.text: pygame.Surface = font.render(text, True, (255, 255, 255))
        self.color = 107, 142, 35

        self.is_hovered = False

    def check_hovered_or_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        if self.is_hovered:
            self.color = 85, 107, 47
        else:
            self.color = 107, 142, 35

        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, self.image.get_width(), self.image.get_height()),border_radius=5)
        font_rect = self.text.get_rect(center=(self.rect.width // 2, self.rect.height // 2 - 10))
        self.image.blit(self.text, font_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(7, 14), Vector2(6, 14), Vector2(5, 14)]
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
        self.blured = False

        self.stroke_panel = pygame.Rect(cell_size * 3, cell_size * 3, (number_of_cells - 6) * cell_size, (number_of_cells - 6) * cell_size)
        self.grid = pygame.image.load('images/grid.png').convert()
        self.bg_blur = pygame.image.load('images/bg_blur.png').convert()
        self.font = pygame.font.Font('fonts/WANTED.ttf', 70)
        self.font2 = pygame.font.Font('fonts/WANTED.ttf', 45)

        self.MOVE_SNAKE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_SNAKE, 200)

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.restart_button = Button((300, 350), (200, 60), 'Restart', self.font, self.buttons)

        self.snake = Snake()
        self.food = None

        self.score = 0
        self.best_score = 0


    def draw(self):
        self.screen.fill((171, 200, 95))
        self.screen.blit(self.grid, (cell_size * 3, cell_size * 3))
        pygame.draw.rect(self.screen, (43, 51, 24), self.stroke_panel, 3, 3)

        for segment in self.snake.body:
            segment_rect = (segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            if segment == self.snake.body[0]:
                pygame.draw.rect(self.screen, '#01796F', segment_rect, border_radius=4)
            else:
                pygame.draw.rect(self.screen, '#4f6015', segment_rect, border_radius=4)

        self.all_sprites.draw(self.screen)

    def check_collision_snake_food(self):
        if self.snake.body[0] == self.food.pos:
            self.food = self.generate_fruit()
            self.snake.body.insert(-1, self.snake.body[-1])
            self.score += 1
            print(self.score)

    def check_collision_edges(self):
        if self.snake.body[0].x == number_of_cells - 3  or self.snake.body[0].x == 2:
            self.game_over = True
        if self.snake.body[0].y == number_of_cells - 3 or self.snake.body[0].y == 2:
            self.game_over = True


    def check_collision_with_tails(self):
        body = self.snake.body[1:]
        if self.snake.body[0] in body:
            self.game_over = True

    def generate_fruit(self):
        if self.food:
            self.food.kill()
        x, y = (randint(3, number_of_cells - 4), randint(3, number_of_cells - 4))
        position = Vector2(x, y)

        while position in self.snake.body:
            x, y = (randint(0, number_of_cells - 1),) * 2
            position = Vector2(x, y)

        return Food(position, self.all_sprites)

    def update(self):
        self.draw()
        self.check_collision_snake_food()
        self.check_collision_with_tails()
        self.all_sprites.update()
        self.check_collision_edges()
        self.draw_score()

    def gaussian_blur(self, radius):
        scaled_surface = pygame.transform.smoothscale(self.screen,(self.screen.get_width() // radius, self.screen.get_height() // radius))
        scaled_surface = pygame.transform.smoothscale(scaled_surface, (self.screen.get_width(), self.screen.get_height()))
        return scaled_surface

    def reset_game(self):
        self.game_over = False
        self.blured = False
        self.snake.body = [Vector2(7, 14), Vector2(6, 14), Vector2(5, 14)]
        self.snake.direction = Vector2(0, 0)
        self.blured = False
        if self.score > self.best_score:
            self.best_score = self.score
        self.score = 0

    def draw_score(self):
        score_text = self.font2.render(f'Score: {self.score}', True, '#333333')
        self.screen.blit(score_text, (cell_size * 3, cell_size))

        best_score_text = self.font2.render(f'Best Score: {self.best_score}', True, '#333333')
        best_score_rect = best_score_text.get_rect(topright=(cell_size * 27, cell_size))
        self.screen.blit(best_score_text, best_score_rect)

    def draw_final_score(self):
        score_text = self.font2.render(f'Final Score: {self.score}', True, '#333333')
        score_rect = score_text.get_rect(center=((cell_size * number_of_cells) // 2, (cell_size * number_of_cells) // 2 - 50))
        self.screen.blit(score_text, score_rect)

        best_score_text = self.font2.render(f'Best Score: {self.best_score}', True, '#333333')
        best_score_rect = best_score_text.get_rect(center=((cell_size * number_of_cells) // 2, (cell_size * number_of_cells) // 2 - 15))
        self.screen.blit(best_score_text, best_score_rect)

    def run(self):
        self.food = Food(Vector2(23, 14), self.all_sprites)
        while self.running:
            if not self.game_over:
                self.update()

                for event in pygame.event.get():
                    if event.type == self.MOVE_SNAKE and not self.game_over:
                        self.snake.update()
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT and self.snake.direction != [-1, 0]:
                            self.snake.direction = Vector2(1, 0)
                        elif event.key == pygame.K_LEFT and self.snake.direction != [1, 0] and self.snake.direction != [0, 0]:
                            self.snake.direction = Vector2(-1, 0)
                        elif event.key == pygame.K_DOWN and self.snake.direction != [0, -1]:
                            self.snake.direction = Vector2(0, 1)
                        elif event.key == pygame.K_UP and self.snake.direction != [0, 1]:
                            self.snake.direction = Vector2(0, -1)

            else:
                self.draw_final_score()
                if not self.blured:
                    self.screen.blit(self.gaussian_blur(cell_size), (0, 0))
                    self.blured = True

                self.buttons.draw(self.screen)
                self.buttons.update()

                mouse_key = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()

                for button in self.buttons: # type: Button
                    button.is_hovered = button.check_hovered_or_clicked(mouse_pos)
                    if mouse_key[0] and button.check_hovered_or_clicked(mouse_pos):
                        self.reset_game()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()