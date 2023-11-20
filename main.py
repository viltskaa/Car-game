import pygame

import config
from Sprites.Car import Car

pygame.init()
pygame.font.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

screen = pygame.display.set_mode(
    (config.WIDTH, config.HEIGHT)
)

car = Car()
car_group = pygame.sprite.Group()
car_group.add(car)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(config.FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    car_group.update()

    screen.fill((0, 0, 0))
    car_group.draw(screen)
    car.draw_vector(screen)

    pygame.display.flip()

pygame.quit()
