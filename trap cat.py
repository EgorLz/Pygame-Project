import os
import sys

import pygame
import random

pygame.display.set_icon(pygame.image.load("./data/icon.png"))
pygame.init()
size = width, height = 970, 500
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


all_sprites = pygame.sprite.Group()


class Pole(pygame.sprite.Sprite):
    pole = load_image("pole.png")
    pole_close = load_image("pole_close.png")

    def __init__(self, x, y, is_active=True, *group):
        super().__init__(*group)
        self.image = Pole.pole if is_active else Pole.pole_close
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = Pole.pole_close


class Cat(pygame.sprite.Sprite):
    image = load_image("cat_stay.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Cat.image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


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
                Pole(x, y, True, all_sprites)
                all_count -= 1
            else:
                Pole(x, y, False, all_sprites)
                all_count -= 1
                count -= 1
        else:
            Pole(x, y, True, all_sprites)
            all_count -= 1

start_pos_x = 430
start_pos_y = 190
Cat(start_pos_x, start_pos_y, all_sprites)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_sprites.update(event)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()