import pygame
import os
import sys


class Gun(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Gun, self).__init__()
        self.screen = screen
        self.image = load_image('gun.png')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.health = 3

    def gun_print(self):
        self.screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, gun):
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 3, 12)
        self.color = (36, 255, 0)
        self.speed = 2
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top

    def update(self):
        self.rect.y -= self.speed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Ufo(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Ufo, self).__init__()
        self.screen = screen
        self.image = load_image('first_chubrick.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.y = self.rect.height
        self.speed = 0.1

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.y += self.speed
        self.rect.y = round(self.y)


def army_create(screen, ufos, k):
    global last_len
    for j in range(5):
        for i in range(7):
            ufo = Ufo(screen)
            ufo.speed *= k
            ufo.rect.x = ufo.rect.width * (i + 1) + 30 * i
            ufo.y = ufo.rect.height * (j + 1) + 30 * (j + 1)
            ufos.add(ufo)
    last_len = 35


def screen_update(screen, gun, ufos, bullets, score, record):
    screen.fill(BLACK)

    bullets.update()

    for bullet in bullets.sprites():
        bullet.draw()
        if bullet.rect.y < 0:
            bullets.remove(bullet)

    pygame.draw.line(screen, RED, (0, 500), (500, 500))

    gun.gun_print()

    for ufo in ufos.sprites():
        ufo.update()
        if ufo.rect.y > 470:
            ufos.remove(ufo)
            gun.health -= 1
            gun.rect.centerx = 250

    ufos.draw(screen)

    for i in range(gun.health):
        health_image = load_image('health.png')
        health_rect = health_image.get_rect()
        health_rect.x = 10 * (i + 1)
        health_rect.y = 7
        screen.blit(health_image, health_rect)

    text = font.render('Счёт: ' + str(int(score)), False, WHITE)
    screen.blit(text, (300, 10))
    text = font.render('Рекорд: ' + str(int(record)), False, WHITE)
    screen.blit(text, (300, 30))


def is_play(gun):
    global k, bullets
    if gun.health > 0:
        if len(ufos) < 1:
            k *= 1.3
            army_create(screen, ufos, k)
            bullets = pygame.sprite.Group()

        return True

    return False


def restart():
    global gun, bullets, ufos, k, move_right, move_left, last_step, score, record

    try:
        f = open('data/data.txt', 'r+')
        f.write(str(round(record)))
    except Exception:
        pass
    f.close()

    try:
        f = open('data/data.txt', 'r+')
        data = f.read().split('/n')
        record = float(data[0])
    except Exception:
        record = 0
        f.write('0')

    f.close()

    end_screen((500, 600), round(score), round(record))

    score = 0

    gun = Gun(screen)
    bullets = pygame.sprite.Group()
    ufos = pygame.sprite.Group()

    army_create(screen, ufos, 1)

    k = 1

    move_right = False
    move_left = False
    last_step = None


def load_image(name, color_key=None):
    fullname = os.path.join('data\images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen_size):
    fon = pygame.transform.scale(load_image('start_screen.png'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


def end_screen(screen_size, score, record):
    intro_text = [
        'Счёт: ' + str(score),
        'Рекорд: ' + str(record),
        'Нажмите любую кнопку, чтобы начать заново'
    ]
    fon = pygame.transform.scale(load_image('start_screen.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10

    for line in intro_text:
        string_rendered = font.render(line, False, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


pygame.init()
font = pygame.font.Font(None, 24)
size = 500, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Звёздные войны')

gun = Gun(screen)
bullets = pygame.sprite.Group()
ufos = pygame.sprite.Group()

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

k = 1
fps = 60
clock = pygame.time.Clock()
running = True
move_right = False
move_left = False
last_step = None
last_len = 35
score = 0
try:
    f = open('data/data.txt', 'r+')
    data = f.read().split('/n')
    record = float(data[0])
except Exception:
    record = 0
    f.write('0')
f.close()

army_create(screen, ufos, 1)

start_screen(size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move_right = True
                last_step = 'right'
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                move_left = True
                last_step = 'left'
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move_right = False
                if move_left:
                    last_step = 'left'
                else:
                    last_step = None
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                move_left = False
                if move_right:
                    last_step = 'right'
                else:
                    last_step = None

    if last_step == 'right':
        gun.rect.centerx += 2 if gun.rect.centerx in range(30, 468) else 0
    elif last_step == 'left':
        gun.rect.centerx -= 2 if gun.rect.centerx in range(32, 469) else 0

    collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)
    score += (last_len - len(ufos)) * k
    score = round(score, 2)
    if score > record:
        record = score
    last_len = len(ufos)
    if is_play(gun):
        screen_update(screen, gun, ufos, bullets, score, record)
    else:
        restart()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
