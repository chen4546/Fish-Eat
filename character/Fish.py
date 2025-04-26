import pygame
import math

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
        self.size = specie['size']
        self.weight=self.size
        # 替换原有image逻辑
        self.base_image = pygame.image.load(f'drawable/png/{self.name}.png').convert_alpha()

        self.base_image = pygame.transform.scale(self.base_image, (self.size, self.size))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=(rect[0], rect[1]))
        # 移动方向相关属性
        self.direction = pygame.math.Vector2(1, 0)  # 默认向右
        self.angle = 0  # 当前旋转角度
        self.rotated_images = {}  # 角度缓存
        self.last_angle = None

    def rotate(self):
        """更精确的旋转计算"""
        if self.direction.length() > 0:
            # 计算角度（注意y轴方向需要取反）
            self.angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))

            # 应用旋转并保持图像质量
            self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)

            # 精确保持中心点
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

    def constrain_position(self):
        """限制鱼的位置在窗口内"""
        self.rect.x = max(0, min(self.rect.x, pixel_x - self.size))
        self.rect.y = max(0, min(self.rect.y, pixel_y - self.size))

    def check_collision(self, other):
        # 使用圆形碰撞检测
        distance = ((self.rect.centerx - other.rect.centerx) ** 2 +
                    (self.rect.centery - other.rect.centery) ** 2) ** 0.5
        return distance < (self.size / 2 + other.size / 2)

