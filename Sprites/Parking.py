import pygame


class Parking(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, angle: int, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((65, 150))
        self.image.set_alpha(25)
        self.image.fill((207, 242, 102))
        self.image = pygame.transform.rotozoom(
            self.image,
            angle,
            1)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.bound = 0
        self.angle = angle

    def update(self, *args, **kwargs):
        virtual_mask = pygame.mask.from_surface(self.image)
        car = kwargs["car"]
        offset = (self.rect.x - car.rect.x, self.rect.y - car.rect.y)
        bounds = car.mask.overlap_area(virtual_mask, offset)
        percent_bounds = bounds / car.mask.count()
        self.bound = percent_bounds

