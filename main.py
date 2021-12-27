import pygame
import random
import os
import sys


class MyScreen:
    def __init__(self):
        self.splashtxt = self.get_text()  # Рандомный сплеш в начале
        self.phase = "start"  # Отвечает за текущий момент прохождения игры, меняется по ходу игры
        self.angle = 3
        self.n_sprites = pygame.sprite.Group()
        self.nchsprite = NLetter(self.n_sprites, 3)
        self.n_sprites.add(self.nchsprite)
        self.all_letters = pygame.sprite.Group()
        pass

    def render(self, screen):  # Основной блок отображения экрана
        if self.phase == "start":
            self.render_start(screen)
        elif self.phase == "first":
            self.render_first(screen)
        elif self.phase == "second":
            self.render_second(screen)

    def render_start(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 310), (1300, 310), (1300, 590), (300, 590)), 7)
        font = pygame.font.Font(None, 230)
        text = font.render("Это   е игра.", True, (255, 255, 255))
        screen.blit(text, (325, 370))
        self.n_sprites.draw(screen)
        self.render_splash()

    def render_first(self, screen):
        k = self.nchsprite.update()
        self.angle += 3.35
        if self.angle > 90:
            self.angle = 90
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 310), (1300, 310), (1300, 590), (300, 590)), 7)
        font = pygame.font.Font(None, 230)
        text = font.render("Это   е игра.", True, (255, 255, 255))
        screen.blit(text, (325, 370))
        self.render_splash()
        self.nchsprite.change_angle(self.angle)
        self.n_sprites.draw(screen)
        if k[0] is True:
            self.phase = "second"

    def render_second(self, screen):
        self.n_sprites.draw(screen)
        self.render_splash()
        self.all_letters.update()
        self.all_letters.draw(screen)
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 310), (1300, 310), (1300, 590), (300, 590)), 7)
        # Тут уже код вызывается падение остальных буковок, но их пока нет :(
        #  self.all_leters.add(self.bukva1, self.bukva2...)

    def render_splash(self):
        fontforsplash = pygame.font.Font(None, 50)
        splash = fontforsplash.render(self.splashtxt, True, (255, 255, 255))
        screen.blit(splash, (450, 5))

    def get_click(self, mouse_pos):
        k = self.nchsprite.update(event)
        self.splashtxt = k[1]
        self.render_splash()
        if k[0] == 3:
            self.phase = "first"

    def get_text(self):
        texts = ["            И зачем ты сюда пришёл?",
                 "              Ну тут реально нет игры",
                 "Лучше бы разработчика поддержали...",
                 "            Может, ты лучше выйдешь?",
                 "           Только ничего тут не сломай",
                 "             Здесь абсолютно ничего",
                 "                        Текст сверху"]
        k = random.choice(texts)
        return k


class Letter(pygame.sprite.Sprite):
    def __init__(self, group, angle, filename, x, y):
        super().__init__(group)
        self.origimage = filename
        self.image = pygame.transform.rotate(load_image(filename), angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 1
        self.angle = angle

    def drop(self):
        self.rect.y += self.velocity
        self.velocity += 1
        if self.rect.y > 770:
            self.rect.y = 770
            return True
        return None

    def update(self):
        self.drop()

    def change_angle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(load_image(self.origimage), self.angle)


class NLetter(Letter):
    def __init__(self, group, angle):
        super().__init__(group, angle, "N.png", 623, 390)
        self.clickcounter = 0

    def update(self, *args):
        if self.clickcounter == 3:
            return self.drop(), "Всё сломал... Кто тебя вообще пригласил?!"
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.clickcounter += 1
            if self.clickcounter == 3:
                return self.clickcounter, "Всё сломал... Кто тебя вообще пригласил?!"
            return self.clickcounter, "              НИЧЕГО ТУТ НЕ ТРОГАЙ!"
        return self.clickcounter, "     Ты думаешь, тебе это что-то даст?"


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    mainwind = MyScreen()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mainwind.get_click(event.pos)
        screen.fill((30, 30, 40))
        mainwind.render(screen)
        pygame.display.flip()
        clock.tick(50)