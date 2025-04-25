import pygame
from config.Pixel import pixel_x,pixel_y 


class Fish(pygame.sprite.Sprite):
    """
    size:鱼的大小
    color:鱼的颜色
    speed:移动速度
    height:鱼的质量,吃鱼后增加对方的一定质量
    """

    def __init__(self, specie, rect):
        super().__init__()
        self.name = specie['name']
        self.speed = specie['speed']
        self.weight = specie['weight']
        self.size = specie['size']
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=(rect[0], rect[1]))

    def eat(self, other_fish):
        if self.size > other_fish.size:
            self.weight += other_fish.weight
            other_fish.weight = 0
            self.size += other_fish.size//4

            self.image=pygame.Surface((self.size,self.size))
            self.image.fill('green')
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

    def constrain_position(self):
        """限制鱼的位置在窗口内"""
        self.rect.x = max(0, min(self.rect.x, pixel_x - self.size))
        self.rect.y = max(0, min(self.rect.y, pixel_y - self.size))