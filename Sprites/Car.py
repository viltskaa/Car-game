import pygame
import config
import math


class Car(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.images = [
            pygame.image.load("./assets/car.png"),
            pygame.image.load("./assets/car-stop.png")
        ]
        self.images = list(map(
            lambda x: pygame.transform.scale(x, (230 // 4, 560 // 5)),
            self.images
        ))
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.center = (config.WIDTH // 2, config.HEIGHT // 2)

        self.speed = 0
        self.deg = 0  # -50d <= 0 <= 50d
        self.direction = ((0, 0), (0, 0))
        self.calc_vector()

    def update(self, *args, **kwargs):
        key = pygame.key.get_pressed()

        # управление по Y
        if key[pygame.K_w]:
            if self.speed < 20:
                self.speed += 1
        elif self.speed > 0:
            self.speed -= 0.5
        if key[pygame.K_SPACE]:
            if self.speed == 0:
                self.image = self.images[0]
            if self.speed != 0:
                self.image = self.images[1]
                self.speed -= 1 if self.speed > 0 else -1
        if key[pygame.K_s] and self.speed <= 0:
            if self.speed > -5:
                self.speed -= 1
        # управление по X
        if key[pygame.K_a] and self.deg != 50:
            self.deg += 5
        if key[pygame.K_d] and self.deg != -50:
            self.deg -= 5

        self.calc_vector()

    def calc_vector(self):
        self.direction = (self.rect.center,
                          (self.rect.center[0] + (self.deg if self.speed > 0 else 0),
                           self.rect.center[1] + abs(self.speed) * 10)
                          )

    def draw_vector(self, screen: pygame.Surface):
        pygame.draw.line(screen,
                         (255, 255, 255),
                         self.direction[:1],
                         self.direction[1:],
                         3)
        pygame.draw.arc(screen, (0, 255, 0), (
                self.rect.x + self.rect.width + (0 if self.deg >= 0 else self.deg),
                self.rect.center[1],
                abs(self.deg),
                100
        ), math.pi if self.deg > 0 else 1.5 * math.pi, 0 if self.deg < 0 else 1.5 * math.pi)
        pygame.draw.arc(screen, (0, 255, 0), (
            self.rect.x + (0 if self.deg >= 0 else self.deg),
            self.rect.center[1],
            abs(self.deg),
            100
        ), math.pi if self.deg > 0 else 1.5 * math.pi, 0 if self.deg < 0 else 1.5 * math.pi)