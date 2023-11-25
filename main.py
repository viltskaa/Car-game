import random

import pygame
import utils
from Sprites.Car import Car
from Sprites.Parking import Parking
import file_utils

config = file_utils.read_config_json()
# save = file_utils.read_json()

pygame.init()
pygame.mixer.init()
pygame.font.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

screen = pygame.display.set_mode(
    (config['width'], config['height'])
)

car = Car()
car_group = pygame.sprite.Group()
car_group.add(car)
# for data in save:
#     car = Car.parse_json(data)
#     car_group.add(car)

parking = Parking(
    *utils.generate_point(100, config['width'] - 100, 100, config['height'] - 100),
    random.randint(0, 360)
)
parking_group = pygame.sprite.Group()
parking_group.add(parking)

clock = pygame.time.Clock()
running = True

time = 8 * config['framerate']
score = 0

while running:
    clock.tick(config['framerate'])
    if time == 0:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    car_group.update()
    parking_group.update(car=car)
    time -= 1

    if parking.bound >= 0.97:
        score += 1
        time = 8 * config['framerate']
        parking_group.remove(parking)
        parking = Parking(
            *utils.generate_point(100, config['width'] - 100, 100, config['height'] - 100),
            random.randint(0, 360)
        )
        parking_group.add(parking)

    screen.fill(config['colors']['black'])
    parking_group.draw(screen)
    car_group.draw(screen)

    time_rendered = font.render(f"Time: {time / config['framerate']}", True, (255, 255, 255))
    screen.blit(time_rendered, (10, 10))

    bound_rendered = font.render(f"Bound: {parking.bound:.2f}", True, (255, 255, 255))
    screen.blit(bound_rendered, (10, 30))

    bound_rendered = font.render(f"Score: {score}", True, (0, 255, 255))
    screen.blit(bound_rendered, (10, 50))

    pygame.display.flip()

pygame.quit()
