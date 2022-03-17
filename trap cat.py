import os
import sys

import webbrowser
import pygame
import pygame_gui
import random
import time

pygame.display.set_icon(pygame.image.load("./data/icon.png"))
pygame.init()
size = width, height = 1150, 500
FPS = 60
screen = pygame.display.set_mode(size)
background = pygame.Surface((130, 500))
background.fill(pygame.Color('white'))
screen.fill('white')
pygame.display.set_caption('Trap cat by lazzzy')
pygame.mixer.music.load('data/music/inecraft_excuse.mp3')
open_sound = pygame.mixer.Sound('data/music/inecraft_chest_open.mp3')
level_sound = pygame.mixer.Sound("data/music/inecraft_level_u.mp3")
deathe_sound = pygame.mixer.Sound("data/music/inecraft_death.mp3")
pygame.mixer.music.play()

manager = pygame_gui.UIManager((1150, 500))

start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1035, 110), (100, 50)),
                                         text='Start',
                                         manager=manager)

diifculti1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1060, 160), (50, 50)),
                                          text='1',
                                          manager=manager)

diifculti2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1060, 210), (50, 50)),
                                          text='2',
                                          manager=manager)

diifculti3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1060, 260), (50, 50)),
                                          text='3',
                                          manager=manager)

diifculti4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1060, 310), (50, 50)),
                                          text='4',
                                          manager=manager)

diifculti5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1060, 360), (50, 50)),
                                          text='5',
                                          manager=manager)

info_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1110, 460), (40, 40)),
                                        text='?',
                                        manager=manager)


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


def info_screen():
    intro_text = ["Правила:",
                  "Кликая по клеточкам вы не даете ",
                  "кошке на них прыгать",
                  "Задача: поймать кошку так, чтобы",
                  " она не могла никуда пойти"]

    return_text = ["Нажмите ` для выхода"]
    pygame.display.set_mode((500, 500))
    pygame.display.set_caption('INFO by lazzzy')
    fon = pygame.transform.scale(load_image('info.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 25)
    text_coord = height // 4 + 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('Green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    for line in return_text:
        font = pygame.font.Font(None, 25)
        string_rendered = font.render(line, 1, pygame.Color('Black'))
        screen.blit(string_rendered, (125, 400))

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
pole_group = pygame.sprite.Group()
music_group = pygame.sprite.Group()
endofgame_group = pygame.sprite.Group()
vk_group = pygame.sprite.Group()
hero = pygame.sprite.Group()

board = [['0'] * 11 for _ in range(11)]


class VK(pygame.sprite.Sprite):
    image = load_image("VK.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = VK.image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            webbrowser.open("https://vk.com/gordei_vk", new=2)


class Music(pygame.sprite.Sprite):
    is_active = True
    svyk = load_image("+звук.jpg")
    svykno = load_image("-звук.jpg")

    def __init__(self, x, y, is_active=True, *group):
        super().__init__(*group)
        self.image = Music.svyk
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x

    def update(self, *args):
        global start_time
        if args and self.rect.collidepoint(args[0].pos):
            if time.time() - start_time >= 0.4:
                start_time = time.time()
                if Music.is_active:
                    self.image = Music.svykno
                    Music.is_active = False
                    pygame.mixer.music.set_volume(0)
                else:
                    self.image = Music.svyk
                    Music.is_active = True
                    pygame.mixer.music.set_volume(1)


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
        if args and self.rect.collidepoint(args[0].pos):
            if time.time() - start_time >= 0.4:
                self.image = Pole.pole_close
                start_time = time.time()
                board[self.pos_y][self.pos_x] = '1'
                if self.pos_y == 10 and self.pos_x == 10:
                    webbrowser.open("https://www.youtube.com/watch?v=zLdHDOdpIeU", new=2)


class Cat(pygame.sprite.Sprite):
    image = load_image("cat_stay.png")
    image_r = load_image("cat_stay_r.png")

    global cat_y, cat_x

    def __init__(self, cat_x, cat_y, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = Cat.image
        self.rect = self.image.get_rect()
        self.rect.y = cat_y
        self.rect.x = cat_x
        self.pos_x = pos_x
        self.pos_y = pos_y

    def check_pole_l(self):
        if board[self.pos_y][self.pos_x - 1] == '0':
            return True
        else:
            return False

    def check_pole_lh(self):
        if self.pos_y % 2 == 1:
            if board[self.pos_y - 1][self.pos_x - 1] == '0':
                return True
            else:
                return False
        else:
            if board[self.pos_y - 1][self.pos_x] == '0':
                return True
            else:
                return False

    def check_pole_ll(self):
        if self.pos_y % 2 == 1:
            if board[self.pos_y + 1][self.pos_x - 1] == '0':
                return True
            else:
                return False
        else:
            if board[self.pos_y + 1][self.pos_x] == '0':
                return True
            else:
                return False

    def check_pole_r(self):
        if board[self.pos_y][self.pos_x + 1] == '0':
            return True
        else:
            return False

    def check_pole_rh(self):
        if self.pos_y % 2 == 1:
            if board[self.pos_y - 1][self.pos_x] == '0':
                return True
            else:
                return False
        else:
            if board[self.pos_y - 1][self.pos_x + 1] == '0':
                return True
            else:
                return False

    def check_pole_rl(self):
        if self.pos_y % 2 == 1:
            if board[self.pos_y + 1][self.pos_x] == '0':
                return True
            else:
                return False
        else:
            if board[self.pos_y + 1][self.pos_x + 1] == '0':
                return True
            else:
                return False

    def move_l(self):
        self.rect.x -= 85
        self.pos_x -= 1

    def move_lh(self):
        if self.pos_y % 2 == 1:
            self.pos_x -= 1
        self.pos_y -= 1
        self.rect.x -= 40
        self.rect.y -= 45

    def move_ll(self):
        if self.pos_y % 2 == 1:
            self.pos_x -= 1
        self.pos_y += 1
        self.rect.x -= 40
        self.rect.y += 45

    def move_r(self):
        self.rect.x += 85
        self.pos_x += 1

    def move_rh(self):
        if self.pos_y == 0:
            self.pos_x += 1
        self.pos_y -= 1
        self.rect.x += 40
        self.rect.y -= 45

    def move_rl(self):
        if self.pos_y == 0:
            self.pos_x += 1
        self.pos_y += 1
        self.rect.x += 42
        self.rect.y += 45

    def update(self):
        if self.check_pole_l():
            self.move_l()
            self.image = Cat.image
        elif self.check_pole_lh():
            self.move_lh()
            self.image = Cat.image
        elif self.check_pole_ll():
            self.move_ll()
            self.image = Cat.image
        elif self.check_pole_r():
            self.move_r()
            self.image = Cat.image_r
        elif self.check_pole_rh():
            self.move_rh()
            self.image = Cat.image_r
        elif self.check_pole_rl():
            self.move_rl()
            self.image = Cat.image_r
        else:
            EndOfGame(300, 20, True, all_sprites, endofgame_group)

    def restart(self):
        self.rect.x = 430
        self.rect.y = 190
        self.pos_x = 5
        self.pos_y = 5


class EndOfGame(pygame.sprite.Sprite):
    loser = load_image("at-winer.png")
    winner = load_image("at-looser.png")

    def __init__(self, x, y, is_win=False, *group):
        super().__init__(*group)
        self.image = EndOfGame.winner if is_win else EndOfGame.loser
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


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
                if i == 5 and j == 5:
                    Pole(x, y, j, i, True, all_sprites, pole_group)
                    all_count -= 1
                else:
                    Pole(x, y, j, i, False, all_sprites, pole_group)
                    board[i][j] = 1
                    all_count -= 1
                    count -= 1
            else:
                Pole(x, y, j, i, True, all_sprites, pole_group)
                all_count -= 1


def make_music():
    Music(1000, 450, True, all_sprites, music_group)


def VK_open():
    VK(1090, 10, all_sprites, vk_group)


def loss():
    EndOfGame(300, 50, False, all_sprites, endofgame_group)


def group_clear():
    endofgame_group.empty()
    pole_group.empty()
    for sprite in all_sprites:
        if isinstance(sprite, EndOfGame) or isinstance(sprite, Pole):
            all_sprites.remove(sprite)


poscat_x = 430
poscat_y = 190
cat_x = 5
cat_y = 5

start_time = time.time()

clock = pygame.time.Clock()


def main():
    global board
    board = [['0'] * 11 for _ in range(11)]
    last_time = time.time()
    running = True
    n = 8
    start_screen()
    drawpole(n)
    make_music()
    VK_open()
    cat = Cat(poscat_x, poscat_y, cat_x, cat_y, hero)
    while running:
        time_delta = clock.tick(60) / 1000.0
        clock.tick(FPS)
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                n = 10
                if event.ui_element == diifculti1:
                    n = 15
                    open_sound.play()
                if event.ui_element == diifculti2:
                    n = 10
                    open_sound.play()
                if event.ui_element == diifculti3:
                    n = 8
                    open_sound.play()
                if event.ui_element == diifculti4:
                    n = 7
                    open_sound.play()
                if event.ui_element == diifculti5:
                    n = 6
                    open_sound.play()
                if event.ui_element == start_btn:
                    group_clear()
                    cat.restart()
                    level_sound.play()
                    board = [['0'] * 11 for _ in range(11)]
                    drawpole(n)
                if event.ui_element == info_btn:
                    open_sound.play()
                    info_screen()
                    pygame.display.set_mode(size)
            manager.process_events(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                vk_group.update(event)
                pole_group.update(event)
                music_group.update(event)
                if event.type != pygame_gui.UI_BUTTON_PRESSED:
                    try:
                        if cat.pos_x < 0 or cat.pos_x > 10:
                            loss()
                        if cat.pos_y < 0 or cat.pos_y > 10:
                            loss()
                        if time.time() - last_time >= 0.4:
                            last_time = time.time()
                        hero.update()
                    except IndexError:
                        pass
        screen.blit(background, (970, 0))
        screen.fill("white")
        all_sprites.draw(screen)
        hero.draw(screen)
        all_sprites.update()
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
