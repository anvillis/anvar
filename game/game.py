import math
import os
import sys

import pygame

pygame.init()

# 1. Окно
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Машинка на pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")
SCALE = 4  # пиксельная графика: увеличиваем в 4 раза БЕЗ сглаживания


# 2. Картинки Kenney (PNG без фона). Машинки в файлах смотрят ВПРАВО.
def load(path):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    # transform.scale = "по ближайшему пикселю", поэтому пиксели остаются чёткими
    return pygame.transform.scale(img, (w * SCALE, h * SCALE))


names = sorted(f[:-4] for f in os.listdir(IMG) if f.endswith(".png"))
cars = [load(os.path.join(IMG, n + ".png")) for n in names]
car_index = names.index("sports_red") if "sports_red" in names else 0

# 3. Управление и состояние
x, y = WIDTH / 2, HEIGHT / 2
speed = 5
facing_right = True
frame = 0


def draw_background():
    screen.fill((110, 180, 100))                      # трава
    pygame.draw.rect(screen, (70, 75, 85), (0, 200, WIDTH, 260))   # дорога
    pygame.draw.rect(screen, (235, 235, 235), (0, 200, WIDTH, 6))  # край дороги
    pygame.draw.rect(screen, (235, 235, 235), (0, 454, WIDTH, 6))
    for lx in range(0, WIDTH, 80):                    # разметка
        pygame.draw.rect(screen, (240, 210, 70), (lx + 10, 327, 44, 6))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:   # следующая машинка
                car_index = (car_index + 1) % len(cars)
            if event.key == pygame.K_z:       # предыдущая машинка
                car_index = (car_index - 1) % len(cars)

    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

    moving = bool(dx or dy)
    if moving:
        length = math.hypot(dx, dy)
        x += dx / length * speed
        y += dy / length * speed
        frame += 1
        if dx:
            facing_right = dx > 0

    car = cars[car_index]
    if not facing_right:
        car = pygame.transform.flip(car, True, False)

    # "анимация": пока машинка едет, она дрожит на 1 пиксель (как работающий мотор)
    shake = SCALE if moving and (frame // 3) % 2 else 0

    rect = car.get_rect(center=(x, y))
    rect.clamp_ip(screen.get_rect())
    x, y = rect.center

    draw_background()
    # тень под машинкой
    shadow = pygame.Surface((rect.width, 14), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 70), shadow.get_rect())
    screen.blit(shadow, (rect.left, rect.bottom - 8))
    screen.blit(car, rect.move(0, -shake))

    text = f"{names[car_index]}  |  Стрелки/WASD - ехать, Пробел/Z - сменить машину, Esc - выход"
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
