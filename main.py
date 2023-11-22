import pygame
from Sprites.Car import Car
import file_utils

config = file_utils.read_config_json()

pygame.init()
pygame.font.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

screen = pygame.display.set_mode(
    (config['width'], config['height'])
)

car = Car()
car_group = pygame.sprite.Group()
car_group.add(car)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(config['framerate'])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            obj = car.to_dict()
            file_utils.write_json(obj)
            running = False
    car_group.update()

    screen.fill(config['colors']['black'])
    car_group.draw(screen)

    pygame.display.flip()

pygame.quit()
