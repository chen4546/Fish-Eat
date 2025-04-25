import random

from character.Fish import Fish
from config.Pixel import pixel_x,pixel_y

class FishComputer(Fish):

    def __init__(self, specie, rect, direction_x=0, direction_y=0):
        super().__init__(specie, rect)
        self.direction_x = direction_x  # 新增：x轴移动方向（-1左, 1右）
        self.direction_y = direction_y  # 新增：y轴移动方向（-1上, 1下）
        self.is_out_of_bounds = False  # 越界标记

    def update(self, keys=None):
        # 根据方向移动，而非随机移动
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        #self.constrain_position()
        self.check_out_of_bounds()

    def check_out_of_bounds(self):
        """根据移动方向检测是否越界，返回是否需销毁"""
        if self.direction_x == 1:  # 向右移动
            self.is_out_of_bounds = (self.rect.left > pixel_x)
        elif self.direction_x == -1:  # 向左移动
            self.is_out_of_bounds = (self.rect.right < 0)
        if self.direction_y == 1:  # 向下移动
            self.is_out_of_bounds = (self.rect.top > pixel_y)
        elif self.direction_y == -1:  # 向上移动
            self.is_out_of_bounds = (self.rect.bottom < 0)