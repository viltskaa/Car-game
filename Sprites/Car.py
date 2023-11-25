import pygame
import file_utils
import math

config = file_utils.read_config_json()
# display_rect = pygame.Rect(0, 0, config["width"], config["height"])
display_mask = pygame.mask.from_surface(pygame.Surface((config["width"], config["height"])))


class Car(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.images = [
            pygame.image.load("./assets/car.png"),
            pygame.image.load("./assets/car-stop.png")
        ]
        self.images = list(map(
            lambda x: pygame.transform.scale(
                pygame.transform.rotate(x, 180),
                (58, 120)
            ),
            self.images
        ))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)

        self.rect.center = (config['width'] // 2, config['height'] // 2)

        self.speed = 0
        self.heading = -math.pi / 2
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(*self.rect.topleft)

    def update(self, *args, **kwargs):
        key = pygame.key.get_pressed()
        if abs(self.speed) > 0:
            self.speed -= 0.2 * (abs(self.speed) // self.speed)

        # управление по Y
        if key[pygame.K_w]:
            self.accelerate(1)
        if key[pygame.K_s]:
            self.accelerate(-1)
        if key[pygame.K_SPACE]:
            self.brake(1.05)
        # управление по X
        if key[pygame.K_a]:
            self.turn(1.8)
        if key[pygame.K_d]:
            self.turn(-1.8)

        self.velocity.from_polar(
            (self.speed,
             math.degrees(math.pi - self.heading))
        )
        virual_rect = self.image.get_rect()
        virual_rect.center = self.position + self.velocity
        in_bounds = display_mask.overlap_area(self.mask, virual_rect.topleft)

        if in_bounds == self.mask.count():
            self.position += self.velocity
            new_coord = (round(self.position[0]), round(self.position[1]))
            self.rect.center = new_coord
        else:
            self.velocity.update(0, 0)
            self.speed = 0

    def turn(self, angle):
        if self.speed == 0:
            return
        self.heading += math.radians(angle)
        x, y = self.rect.center
        self.image = pygame.transform.rotozoom(
            self.images[0],
            math.degrees(self.heading + math.pi / 2),
            1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def brake(self, value):
        if self.speed == 0:
            return
        self.speed /= value
        if abs(self.speed) < 0.1:
            self.speed = 0

    def accelerate(self, value):
        self.speed += value

    @property
    def hitbox(self):
        surface = pygame.Surface(self.rect.size)
        surface.fill(config['colors']['red'])
        surface.set_alpha(30)
        return surface

    def to_json(self):
        return {
            "postions": self.rect.center,
            "speed": 0
        }

    @staticmethod
    def parse_json(json: dict):
        car = Car()
        car.rect.center = json["postions"]
        car.velocity.update(json["speed"])
        car.turn(json["angle"])
        return car


