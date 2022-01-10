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
        self.trashbin = DroppingObject(self.trashbin_group, "trashbin.png", 1380, 650, 650)

        self.planks = pygame.sprite.Group()
        self.plank = DroppingObject(self.planks, "board_new.png", 500, 350, 650)
        self.plank.change_angle(350)
        self.saw_group = pygame.sprite.Group()
        self.saw = DroppingObject(self.saw_group, "saw.png", -40, 650, 850)
        self.saw.image = pygame.transform.flip(self.saw.image, True, False)
        self.saw.canbemoved = True
        self.saw.otkl = 15
        self.scale = 1

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
        elif self.phase == "sixth":
            self.render_sixth(screen)
        elif self.phase == "seventh":
            self.render_seventh(screen)
        elif self.phase == "eighth":
            self.render_eighth(screen)
        elif self.phase == "ninth":
            self.render_ninth(screen)

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
        sp = []
        sp.extend([self.bukvae_a, self.bukvae_e, self.bukvae_ea, self.bukvae_g,
                   self.bukvae_i, self.bukvae_o, self.bukvae_r, self.bukvae_t, self.nchsprite])
        for elem in sp:
            if elem.rect.collidepoint(1500, 770):
                elem.kill()
                elem.iskilled = True
        if all([elem.get_state()[0] for elem in sp]):
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
            self.splashtxt = "      Ты меня не понял?! УХОДИ!"
            self.phase = "fifth"
            self.render(screen)
            self.trashbin.canbemoved = False

    def render_fifth(self, screen):
        self.render_splash()
        self.trashbin_group.update()
        self.trashbin_group.draw(screen)
        self.button_group.update(event)
        self.button_group.draw(screen)
        self.planks.draw(screen)
        self.saw_group.update()
        self.saw_group.draw(screen)
        if self.saw.rect.colliderect(500, 350, 770, 380):
            self.splashtxt = "          Чёт пила у тебя маловата :)"
            self.phase = "sixth"

    def render_sixth(self, screen):
        self.render_splash()
        self.trashbin_group.update()
        self.trashbin_group.draw(screen)
        self.button_group.update(event)
        self.button_group.draw(screen)
        self.planks.draw(screen)
        self.saw_group.update()
        self.saw_group.draw(screen)
        if self.saw.rect.collidepoint(pygame.mouse.get_pos()) and \
                pygame.mouse.get_pressed(num_buttons=3)[0] and \
                pygame.mouse.get_pressed(num_buttons=3)[2]:
            self.saw.image = pygame.transform.scale(self.saw.image, (150 * self.scale, 64 * self.scale))
            self.scale += 0.05
            self.saw.otkl += 2
            self.saw.floor *= 0.995
        if self.scale >= 2:
            self.phase = "seventh"
            self.splashtxt = "ЭЭЭЭЭ, ОСТАНОВИСЬ ПОКА НЕ ПОЗДНО"

    def render_seventh(self, screen):
        self.render_splash()
        self.trashbin_group.update()
        self.trashbin_group.draw(screen)
        self.button.update(event)
        self.button_group.draw(screen)
        self.saw_group.update()
        self.saw_group.draw(screen)
        self.planks.draw(screen)
        if self.saw.rect.colliderect((500, 350, 1000, 500)) and not self.saw.get_state()[0]:
            self.saw.kill()
            self.saw.iskilled = True
            self.plank.kill()
            self.plank.iskilled = True
            self.part1 = DroppingObject(self.planks, "board_part1_new.png", 500, 350, 700)
            self.part1.change_angle(350)
            self.part1.canbemoved = True
            self.part2 = DroppingObject(self.planks, "board_part2_new.png", 750, 450, 700)
            self.part2.change_angle(350)
            self.part2.canbemoved = True
            self.angle1 = 350
            self.angle2 = 350
        if self.saw.get_state()[0]:
            self.planks.update()
            binx = self.trashbin.rect.x
            biny = self.trashbin.rect.y
            if self.part1.rect.y < 700 and not self.part1.get_state()[1]:
                self.angle1 -= 1
                self.part1.change_angle(self.angle1)
            if self.part2.rect.y < 700 and not self.part2.get_state()[1]:
                self.part2.change_angle(self.angle2)
                self.angle2 += 1
            if self.angle1 <= -10 or self.angle2 >= 710:
                self.splashtxt = "Хватит их уже крутить, верни всё на место!"
            if self.part1.rect.colliderect(binx, biny, binx + 256, biny + 256):
                self.part1.kill()
                self.part1.iskilled = True
            if self.part2.rect.colliderect(binx, biny, binx + 256, biny + 256):
                self.part2.kill()
                self.part2.iskilled = True
            if self.part1.get_state()[0] and self.part2.get_state()[0]:
                self.phase = "eighth"
                self.splashtxt = "       ТОЛЬКО НИЧЕГО НЕ ЖМИ!"
                self.button.canbeclicked = True
                self.button.update(event)

    def render_eighth(self, screen):
        self.render_splash()
        self.trashbin_group.update()
        self.trashbin_group.draw(screen)
        k = self.button.update(event)
        self.button_group.draw(screen)
        if k is True:
            self.phase = "ninth"
            self.splashtxt = "Вставьте текст"
            self.button.canbeclicked = False
            self.button.update(event)

    def render_ninth(self, screen):
        self.render_splash()
        self.trashbin_group.draw(screen)
        self.button_group.draw(screen)

    def render_splash(self):
        fontforsplash = pygame.font.Font(None, 50)
        splash = fontforsplash.render(self.splashtxt, True, (255, 255, 255))
        screen.blit(splash, (450, 5))

    def get_click(self, event):
        if self.phase == "start":
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
    def __init__(self, group, filename, x, y, floor):
        super().__init__(group)
        self.origimage = filename
        self.image = load_image(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 1
        self.canbemoved = False
        self.angle = 0
        self.floor = floor
        self.otkl = 120
        self.iskilled = False
        self.ispicked = False

    def drop(self):
        self.rect.y += self.velocity
        self.velocity += 1
        if self.rect.y > self.floor:
            self.rect.y = self.floor
            self.velocity = 1

    def move(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and \
                pygame.mouse.get_pressed(num_buttons=3)[0] is True:
            self.rect.y = pygame.mouse.get_pos()[1] - self.otkl
            self.rect.x = pygame.mouse.get_pos()[0] - self.otkl
            self.velocity = 1
            self.ispicked = True
        else:
            self.ispicked = False
            self.drop()

    def update(self, *args):
        if self.canbemoved is True:
            self.move()
        else:
            self.drop()

    def change_angle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(load_image(self.origimage), self.angle)

    def get_state(self):
        return self.iskilled, self.ispicked


class Letter(DroppingObject):
    def __init__(self, group, angle, filename, x, y):
        super().__init__(group, filename, x, y, 650)
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
        self.canbeclicked = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and self.canbeclicked:
            self.image = self.pressed
            return True
        else:
            self.image = self.notpressed
            return False


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
                mainwind.get_click(event)
        screen.fill((30, 30, 40))
        mainwind.render(screen)
        particle_sprites.update()
        particle_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)
