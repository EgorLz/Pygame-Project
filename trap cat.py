import os
import sys

import pygame
import random
import time

pygame.display.set_icon(pygame.image.load("./data/icon.png"))
pygame.init()
size = width, height = 970, 500
FPS = 60
screen = pygame.display.set_mode(size)
screen.fill('white')
pygame.display.set_caption('Trap cat by lazzzy')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Press space"]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = height // 4 * 3
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
board = [[0] * 11 for _ in range(11)]


class Pole(pygame.sprite.Sprite):
    pole = load_image("pole.png")
    pole_close = load_image("pole_close.png")

    def __init__(self, x, y, pos_x, pos_y, is_active=True, *group):
        super().__init__(*group)
        self.image = Pole.pole if is_active else Pole.pole_close
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self, *args):
        global start_time
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if time.time() - start_time >= 0.7:
                self.image = Pole.pole_close
                start_time = time.time()


class Cat(pygame.sprite.Sprite):
    image = load_image("cat_stay.png")

    def __init__(self, x, y, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = Cat.image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.pos_x = pos_x
        self.pos_y = pos_y


    def check_pole(self):
        if board[self.pos_y][self.pos_x - 1] == 0:
            self.pos_x -= 1
            self.rect.x -= 80

for i in range(11):
    for j in range(11):
        y = 45 * i
        if i % 2 == 1:
            x = 0 + j * 85
        else:
            x = 40 + j * 85
        count = 8
        all_count = 121
        if random.randint(1, all_count) <= count:
            if i == 6 and j == 6:
                Pole(x, y, j, i, True, all_sprites)
                all_count -= 1
            else:
                Pole(x, y, j, i, False, all_sprites)
                board[i][j] = 1
                all_count -= 1
                count -= 1
        else:
            Pole(x, y, j, i, True, all_sprites)
            all_count -= 1

pos_x = 430
pos_y = 190
cat_x = 6
cat_y = 6
Cat(pos_x, pos_y, cat_x, cat_y, all_sprites)

start_time = time.time()

running = True

clock = pygame.time.Clock()
start_screen()
while running:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        all_sprites.update(event)
        Cat.check_pole(Cat(pos_x, pos_y, cat_x, cat_y, all_sprites))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
