import os
import sys

import pygame

pygame.init()
size = width, height = 960, 500
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

all_sprites = pygame.sprite.Group()

class Pole(pygame.sprite.Sprite):
        image = load_image("pole.png")

        def __init__(self, x, y, *group):
            super().__init__(*group)
            self.image = Pole.image
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
        Pole(x, y, all_sprites)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()