import pygame
import random
import os
import sys


class MyScreen:
    def __init__(self):
        self.splashtxt = self.get_text()  # Рандомный сплеш в начале
        self.phase = "start"  # Отвечает за текущий момент прохождения игры, меняется по ходу игры
        self.imagen = load_image("N.png")
        self.firstcounter = 0
        self.yposfirst = 370
        self.velocity = 1
        self.yposch = 413
        self.angle = 3
        self.velocitych = 1
        self.nflag = False
        self.firstdrop = False
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
        all_sprites = pygame.sprite.Group()
        nchsprite = Nch(all_sprites)
        all_sprites.add(nchsprite)
        all_sprites.draw(screen)
        self.render_splash()

    def render_first(self, screen):
        if self.nflag is False:
            self.velocitych += 1
            self.yposch += self.velocitych
            self.angle += 3.35
            if self.yposch > 810:
                self.yposch = 810
                self.angle = 90
                self.nflag = True
        else:
            if self.firstdrop is True:  # Система ускорений, отвечающая за падение начальной надписи
                self.velocity = -13
                self.yposfirst += self.velocity
                self.firstdrop = None
            if self.yposfirst < 755 and self.nflag is True:
                self.velocity += 1
                self.yposfirst += self.velocity
                if self.yposfirst > 755:
                    self.yposfirst = 755
            else:
                self.yposfirst = 755
                if self.firstdrop is False:
                    self.firstdrop = True
                else:
                    self.phase = "second"
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 310), (1300, 310), (1300, 590), (300, 590)), 7)
        font = pygame.font.Font(None, 230)
        text = font.render("Это   е игра.", True, (255, 255, 255))
        screen.blit(text, (325, self.yposfirst))
        self.render_splash()
        all_sprites = pygame.sprite.Group()
        nchsprite = Nch(all_sprites)
        nchsprite.rect.y = self.yposch
        nchsprite.image = pygame.transform.rotate(self.imagen, self.angle)
        all_sprites.add(nchsprite)
        all_sprites.draw(screen)

    def render_second(self, screen):
        self.render_first(screen)

    def render_splash(self):
        fontforsplash = pygame.font.Font(None, 50)
        splash = fontforsplash.render(self.splashtxt, True, (255, 255, 255))
        screen.blit(splash, (450, 5))

    def get_click(self, mouse_pos):
        if self.phase == "start" and 650 < mouse_pos[0] < 738 and 411 < mouse_pos[1] < 497 and self.firstcounter == 2:
            self.splashtxt = "Всё сломал... Кто тебя вообще пригласил?!"
            self.render_splash()
            self.phase = "first"
            self.render(screen)
        elif self.phase == "start" and 650 < mouse_pos[0] < 738 and 411 < mouse_pos[1] < 497:
            self.splashtxt = "              НИЧЕГО ТУТ НЕ ТРОГАЙ!"
            self.firstcounter += 1
            self.render_splash()
        elif self.phase == "start":
            self.splashtxt = "     Ты думаешь, тебе это что-то даст?"
            self.render_splash()
        pass

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


class Nch(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.rotate(load_image("N.png"), 3)
        self.rect = self.image.get_rect()
        self.rect.x = 655
        self.rect.y = 413


def load_image(name, colorkey=(30, 30, 40)):
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

print("КУ")
print("КУ всем КУ")
