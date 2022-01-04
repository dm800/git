import pygame
import random
import os
import sys


class MyScreen:
    def __init__(self):
        self.splashtxt = self.get_text()  # Рандомный сплеш в начале
        self.phase = "start"

        # self.phase = "start"  # Отвечает за текущий момент прохождения игры, меняется по ходу игры
        self.angle = 3
        self.n_sprites = pygame.sprite.Group()
        self.nchsprite = NLetter(self.n_sprites, 3)
        self.n_sprites.add(self.nchsprite)
        self.all_letters = pygame.sprite.Group()
        self.bukvae_ea = Letter(self.all_letters, 0, "Э.png", 340, 390)
        self.bukvae_t = Letter(self.all_letters, 0, "т.png", 415, 390)
        self.bukvae_o = Letter(self.all_letters, 0, "о.png", 490, 390)
        self.bukvae_e = Letter(self.all_letters, 0, "е.png", 765, 390)
        self.bukvae_i = Letter(self.all_letters, 0, "и.png", 915, 390)
        self.bukvae_g = Letter(self.all_letters, 0, "г.png", 990, 390)
        self.bukvae_r = Letter(self.all_letters, 0, "р.png", 1065, 390)
        self.bukvae_a = Letter(self.all_letters, 0, "а.png", 1140, 390)

        self.trashbin_group = pygame.sprite.Group()
        self.trashbin = DroppingObject(self.trashbin_group, "trashbin.png", 1380, 650)

        self.planks = pygame.sprite.Group()
        self.plank = DroppingObject(self.planks, "plank.png", 650, 400)
        self.plank.change_angle(350)

        self.button_group = pygame.sprite.Group()
        self.button = ButtonStart(self.button_group, 680, 395)

    def render(self, screen):  # Основной блок отображения экрана
        if self.phase == "start":
            self.render_start(screen)
        elif self.phase == "first":
            self.render_first(screen)
        elif self.phase == "second":
            self.render_second(screen)
        elif self.phase == "third":
            self.render_third(screen)
        elif self.phase == "fourth":
            self.render_fourth(screen)
        elif self.phase == "fifth":
            self.render_fifth(screen)

    def render_start(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 335), (1300, 335), (1300, 570), (300, 570)), 7)
        self.all_letters.draw(screen)
        self.n_sprites.draw(screen)
        self.render_splash()

    def render_first(self, screen):
        k = self.nchsprite.update()
        self.angle += 3.35
        if self.angle > 90:
            self.angle = 90
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 335), (1300, 335), (1300, 570), (300, 570)), 7)
        self.all_letters.draw(screen)
        self.render_splash()
        self.nchsprite.change_angle(self.angle)
        self.n_sprites.draw(screen)
        if k[0] is True:
            create_particles((740, 850))
            self.phase = "second"

    def render_second(self, screen):
        self.n_sprites.draw(screen)
        self.render_splash()
        self.all_letters.update()
        self.all_letters.draw(screen)
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 335), (1300, 335), (1300, 570), (300, 570)), 7)
        if self.bukvae_a.rect.y >= 770:
            create_particles((self.bukvae_a.rect.y, self.bukvae_a.rect.x))  # Не работает ни капли
            self.phase = "third"
            self.all_letters.add(self.nchsprite)
            sp = []
            sp.extend([self.bukvae_a, self.bukvae_e, self.bukvae_ea, self.bukvae_g,
                       self.bukvae_i, self.bukvae_o, self.bukvae_r, self.bukvae_t, self.nchsprite])
            for elem in sp:
                elem.canbemoved = True

    def render_third(self, screen):
        self.n_sprites.draw(screen)
        self.render_splash()
        self.all_letters.update()
        self.all_letters.draw(screen)
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 335), (1300, 335), (1300, 570), (300, 570)), 7)
        self.splashtxt = "    Прибери за собой и уходи отсюда..."
        self.render_splash()
        self.trashbin_group.update()
        self.trashbin_group.draw(screen)
        c = 0
        sp = []
        sp.extend([self.bukvae_a, self.bukvae_e, self.bukvae_ea, self.bukvae_g,
                   self.bukvae_i, self.bukvae_o, self.bukvae_r, self.bukvae_t, self.nchsprite])
        for elem in sp:
            if elem.rect.collidepoint(1500, 770):
                elem.kill()
                c += 1
        if c == 9:
            self.trashbin.canbemoved = True
            self.phase = "fourth"

    def render_fourth(self, screen):
        self.splashtxt = "                      А теперь уходи"
        self.render_splash()
        pygame.draw.polygon(screen, (255, 255, 255), ((300, 335), (1300, 335), (1300, 570), (300, 570)), 7)
        self.render_splash()
        self.trashbin_group.update()
        self.trashbin_group.draw(screen)
        if self.trashbin.rect.colliderect(300, 335, 900, 235):
            self.phase = "fifth"
            self.render(screen)
            self.trashbin.canbemoved = False

    def render_fifth(self, screen):
        self.splashtxt = "      Ты меня не понял?! УХОДИ!"
        self.render_splash()
        self.trashbin_group.update()
        self.trashbin_group.draw(screen)
        self.button_group.update(event)
        self.button_group.draw(screen)
        self.planks.draw(screen)
        pass

    def render_splash(self):
        fontforsplash = pygame.font.Font(None, 50)
        splash = fontforsplash.render(self.splashtxt, True, (255, 255, 255))
        screen.blit(splash, (450, 5))

    def get_click(self):
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

    def get_phase(self):
        return self.phase


class DroppingObject(pygame.sprite.Sprite):
    def __init__(self, group, filename, x, y):
        super().__init__(group)
        self.origimage = filename
        self.image = load_image(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 1
        self.canbemoved = False
        self.angle = 0

    def drop(self):
        self.rect.y += self.velocity
        self.velocity += 1
        if self.rect.y > 650:
            self.rect.y = 650
            self.velocity = 1

    def move(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and \
                pygame.mouse.get_pressed(num_buttons=3)[0] is True:
            self.rect.y = pygame.mouse.get_pos()[1] - 120
            self.rect.x = pygame.mouse.get_pos()[0] - 120
            self.velocity = 1
        else:
            self.drop()

    def update(self, *args):
        if self.canbemoved is True:
            self.move()
        else:
            self.drop()

    def change_angle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(load_image(self.origimage), self.angle)


class Letter(DroppingObject):
    def __init__(self, group, angle, filename, x, y):
        super().__init__(group, filename, x, y)
        self.origimage = filename
        self.image = pygame.transform.rotate(load_image(filename), angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 1
        self.angle = angle
        self.canbemoved = False

    def drop(self):
        self.rect.y += self.velocity
        self.velocity += 1
        if self.rect.y > 770:
            self.rect.y = 770
            self.velocity = 1

    def move(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and \
                pygame.mouse.get_pressed(num_buttons=3)[0] is True:
            self.rect.y = pygame.mouse.get_pos()[1] - 60
            self.rect.x = pygame.mouse.get_pos()[0] - 60
            self.velocity = 1
        else:
            self.drop()

    def update(self, *args):
        if self.canbemoved is False:
            self.drop()
        else:
            self.move()


class NLetter(Letter):
    def __init__(self, group, angle):
        super().__init__(group, angle, "N.png", 680, 388)
        self.clickcounter = 0

    def drop(self):
        self.rect.y += self.velocity
        self.velocity += 1
        if self.rect.y > 783:
            self.rect.y = 783
            return True
        return None

    def update(self, *args):
        if self.canbemoved is False:
            if self.clickcounter == 3:
                return self.drop(), "Всё сломал... Кто тебя вообще пригласил?!"
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.clickcounter += 1
                if self.clickcounter == 3:
                    return self.clickcounter, "Всё сломал... Кто тебя вообще пригласил?!"
                return self.clickcounter, "              НИЧЕГО ТУТ НЕ ТРОГАЙ!"
            return self.clickcounter, "     Ты думаешь, тебе это что-то даст?"
        else:
            self.move()


class ButtonStart(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = load_image("start.png")
        self.rect = self.image.get_rect()
        self.notpressed = self.image
        self.pressed = load_image("pressed.png")
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.pressed
        else:
            self.image = self.notpressed


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.image.load("data/particles.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, group, pos, dx, dy):
        super().__init__(group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.5

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


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


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 40
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(particle_sprites, position, random.choice(numbers), random.choice(numbers))
    particle_sprites.draw(screen)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1600, 900
    screen_rect = (0, 0, width, height)
    screen = pygame.display.set_mode(size)
    mainwind = MyScreen()
    running = True
    clock = pygame.time.Clock()
    particle_sprites = pygame.sprite.Group()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mainwind.get_phase() == "start":
                    mainwind.get_click()
        screen.fill((30, 30, 40))
        mainwind.render(screen)
        particle_sprites.update()
        particle_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)