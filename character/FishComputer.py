import math
import random
import pygame

from character.Fish import Fish
from config.Pixel import pixel_x, pixel_y


class FishComputer(Fish):

    def __init__(self, game, specie, rect, direction_x=0, direction_y=0):
        super().__init__(specie, rect)
        self.game = game
        self.direction_x = direction_x  # 新增：x轴移动方向（-1左, 1右）
        self.direction_y = direction_y  # 新增：y轴移动方向（-1上, 1下）
        self.is_out_of_bounds = False  # 越界标记

    def update(self, keys=None):
        # 更新移动方向
        move_vector = pygame.math.Vector2(self.direction_x, self.direction_y)
        # 简单追踪玩家逻辑（需在Game类中传递player_fish引用）
        # 概率性追踪玩家
        # print(self.rect)
        if random.random() < 0.02:
            dx = self.game.player_fish.rect.x - self.rect.x
            dy = self.game.player_fish.rect.y - self.rect.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0 and random.random() < 0.3:  # 30%概率追踪玩家
                move_vector = pygame.math.Vector2(dx / distance, dy / distance)
                self.direction_x = move_vector.x
                self.direction_y = move_vector.y

        # 应用移动
        self.rect.x += move_vector.x * self.speed
        self.rect.y += move_vector.y * self.speed
        #print(self.rect.x)
        # 更新方向向量并旋转
        if move_vector.length() > 0:
            self.direction = move_vector
            self.rotate()

        self.check_out_of_bounds()

    def check_out_of_bounds(self):
        """检测是否越界，返回是否需销毁"""
        if self.rect.x > pixel_x + 30 or self.rect.x < -30:
            self.is_out_of_bounds = True
            return
        if self.rect.y > pixel_y + 30 or self.rect.y < -30:
            self.is_out_of_bounds = True
            return
