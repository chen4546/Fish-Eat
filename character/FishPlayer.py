import pygame

from character.Fish import Fish
from config.Pixel import pixel_x, pixel_y


class FishPlayer(Fish):
    def __init__(self, specie, rect):
        super().__init__(specie, rect)
        self.lives = 3  # 初始生命值
        self.is_invincible = False
        self.win = False
        self.invincible_duration = 2000  # 无敌持续时间（毫秒）
        self.invincible_start_time = 0

    def take_damage(self):
        """玩家受到伤害时调用"""
        if not self.is_invincible:
            self.lives -= 1
            self.is_invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

    def update_invincibility(self):
        """更新无敌状态"""
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time > self.invincible_duration:
                self.is_invincible = False

    def update(self, keys):
        if (self.size >= pixel_x or
                self.size >= pixel_y):
            self.win = True
            return
        if self.lives == 0:
            return
        else:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed

        self.constrain_position()
        self.update_invincibility()

    def draw(self, screen):
        """根据无敌状态绘制闪烁效果"""
        if self.is_invincible:
            alpha = 128 if (pygame.time.get_ticks() % 200) < 100 else 255
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        screen.blit(self.image, self.rect)
