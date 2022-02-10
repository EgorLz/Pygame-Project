import os
import sys

import pygame
import pygame_gui
import random
import time

pygame.display.set_icon(pygame.image.load("./data/icon.png"))
pygame.init()
size = width, height = 970, 500
FPS = 60
screen = pygame.display.set_mode(size)
background = pygame.Surface((970, 500))
background.fill(pygame.Color('white'))
screen.fill('white')
pygame.display.set_caption('Trap cat by lazzzy')

manager = pygame_gui.UIManager((970, 500))

# start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((435, 300), (100, 50)),
#                                             text='Start',
#                                             manager=manager)
#
# diifculti1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 200), (50, 50)),
#                                             text='1',
#                                             manager=manager)
#
# diifculti2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 200), (50, 50)),
#                                             text='2',
#                                             manager=manager)
#
# diifculti3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 200), (50, 50)),
#                                             text='3',
#                                             manager=manager)
#
# diifculti4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 200), (50, 50)),
#                                             text='4',
#                                             manager=manager)
#
# diifculti5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 200), (50, 50)),
#                                             text='5',
#                                             manager=manager)


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
    intro_text = ["Press anywhere"]

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
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
hero = pygame.sprite.Group()
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
                board[pos_x][pos_y] = 1


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

    def check_pole_l(self):
        if board[self.pos_y][self.pos_x - 1] == 0:
            return True
        else:
            return False

    def check_pole_lh(self):
        if board[self.pos_y - 1][self.pos_x] == 0:
            return True
        else:
            return False

    def check_pole_ll(self):
        if board[self.pos_y + 1][self.pos_x] == 0:
            return True
        else:
            return False

    def move_l(self):
        self.rect.x -= 85
        self.pos_x -= 1

    def move_lh(self):
        self.pos_y -= 1

    def move_ll(self):
        self.pos_y += 1

    def update(self):
        if self.check_pole_l():
            self.move_l()


n = 8
def drawpole(n):
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

start_time = time.time()

clock = pygame.time.Clock()
def main():
    running = True

    start_screen()
    drawpole(n)
    cat = Cat(pos_x, pos_y, cat_x, cat_y, hero)
    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            # if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #     n = 8
            #     if event.ui_element == diifculti1:
            #         n = 10
            #     if event.ui_element == diifculti2:
            #         n = 8
            #     if event.ui_element == diifculti3:
            #         n = 6
            #     if event.ui_element == diifculti4:
            #         n = 5
            #     if event.ui_element == diifculti5:
            #         n = 4
            #     if event.ui_element == start_btn:
            #         drawpole(n)
            manager.process_events(event)
            all_sprites.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                hero.update()
        all_sprites.draw(screen)
        hero.draw(screen)
        manager.update(time_delta)
        # # screen.blit(background, (0, 0))
        # # manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
