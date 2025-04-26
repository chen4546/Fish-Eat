import pygame

from character.Fish import Fish
from config.Pixel import pixel_x, pixel_y


class FishPlayer(Fish):
    def __init__(self, specie, rect):
        super().__init__(specie, rect)
        self.lives = specie['lives']  # 当前生命值
        self.max_lives=specie['max_lives'] # 最大生命值
        self.stamina=specie['stamina']  # 耐力值
        self.attack_ratio=specie['attack_ratio']# 吞噬系数
        self.regen_rate=specie['regen_rate']# 吞噬系数
        self.growth_stage=specie['growth_stage'] # 成长阶段
        self.current_speed=self.speed
        self.is_invincible = False
        self.win = False
        self.invincible_duration = specie['invincible_duration']  # 无敌持续时间（毫秒）
        self.invincible_start_time = 0
        self.score = 0
        self.win_score=specie['win_score']
        self.original_image=pygame.image.load(f'drawable/png/{self.name}.png').convert_alpha()


    def take_damage(self):
        """玩家受到伤害时调用"""
        if not self.is_invincible:
            self.lives -= 1
            self.score=max(self.score-100,0)
            self.is_invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            return True
        return False


    '''
    def update_invincibility(self):
        """更新无敌状态"""
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time > self.invincible_duration:
                self.is_invincible = False
    '''
    '''
    def update(self, keys):
        if self.score >= 15000:
            self.win=True
            return
        if self.lives == 0:
            return
        # 重置方向向量
        move_vector = pygame.math.Vector2(0, 0)
        # 处理对角线输入
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            move_vector = pygame.math.Vector2(-0.707, -0.707)
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            move_vector = pygame.math.Vector2(-0.707, 0.707)
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            move_vector = pygame.math.Vector2(0.707, -0.707)
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            move_vector = pygame.math.Vector2(0.707, 0.707)
        else:
            # 处理单方向输入
            if keys[pygame.K_LEFT]:
                move_vector.x = -1
            if keys[pygame.K_RIGHT]:
                move_vector.x = 1
            if keys[pygame.K_UP]:
                move_vector.y = -1
            if keys[pygame.K_DOWN]:
                move_vector.y = 1
            if move_vector.length() > 0:
                move_vector = move_vector.normalize()
        # 标准化方向向量（保持对角线移动速度一致）
        if move_vector.length() > 0:
            self.direction = move_vector  # 更新方向向量
            self.rect.x += move_vector.x * self.speed
            self.rect.y += move_vector.y * self.speed

            # 重新应用图像大小
            self.image = pygame.transform.scale(self.base_image, (self.size, self.size))
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

            #print(f"旋转前的方向向量: {self.direction}, 角度: {self.angle}")  # 调试信息
            self.rotate()  # 调用旋转方法
            #print(f"旋转后的方向向量: {self.direction}, 角度: {self.angle}, 图像尺寸: {self.image.get_size()}")  # 调试信息
        self.constrain_position()
        self.update_invincibility()
    '''

    def update(self, keys):
        if self.score>=self.win_score:
            self.win=True
            return
        # 运动控制
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]: move_vector.x -= 1
        if keys[pygame.K_RIGHT]: move_vector.x += 1
        if keys[pygame.K_UP]: move_vector.y -= 1
        if keys[pygame.K_DOWN]: move_vector.y += 1

        # 标准化移动向量
        if move_vector.length() > 0:
            move_vector = move_vector.normalize()
            self.direction = move_vector
            self.rotate()

        # 应用移动
        self.rect.center += move_vector * self.current_speed

        # 耐力系统
        if any(keys):
            self.stamina = max(0, self.stamina - 2)
        else:
            self.stamina = min(100, self.stamina + 0.5)

        self.constrain_position()
        self._update_invincibility()

    def _update_invincibility(self):
        """无敌状态更新"""
        """更新无敌状态"""
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time > self.invincible_duration:
                self.is_invincible = False
    def draw(self, screen):
        """根据无敌状态绘制闪烁效果"""
        current_image = self.image.copy()  # 确保使用当前的image，而不是base_image
        if self.is_invincible:
            alpha = 128 if (pygame.time.get_ticks() % 200) < 100 else 255
            current_image.set_alpha(alpha)
        else:
            current_image.set_alpha(255)
        screen.blit(current_image, self.rect)

    def eat(self, other_fish):
        if self.size > other_fish.size * self.attack_ratio and other_fish.weight != 0:
            other_fish.weight=0
            # 计算基础成长量
            base_growth = other_fish.size * (0.2 - 0.01 * (self.size / 10))
            self.score+=other_fish.size
            new_size = min(self.size + base_growth, 200)
            # 更新属性
            size_diff = new_size - self.size
            self._update_growth(size_diff)
            self.size = new_size

            # 生命恢复
            self.lives = min(self.max_lives, self.lives + 0.15 * self.max_lives)

            # 更新图像
            self._rescale_image()

            # 检查成长阶段
            self._check_growth_stage()

            #从原始图像重新生成缩放后的图像

            self.base_image = pygame.transform.smoothscale(self.original_image, (self.size, self.size))
            self.image = self.base_image.copy()
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

    def _update_growth(self, size_diff):
        """处理成长带来的属性变化"""
        # 速度衰减
        speed_factor = 1 - (self.size / 200) * 0.6
        self.current_speed = self.speed * speed_factor

        # 生命上限提升
        if self.size // 50 > (self.size - size_diff) // 50:
            self.max_lives += 1
            self.lives=self.max_lives
            print(f"解锁新生命上限: {self.max_lives}")

    def _rescale_image(self):
        """图像缩放逻辑"""
        old_center = self.rect.center
        self.image = pygame.transform.smoothscale(
            self.original_image,
            (int(self.size), int(self.size)))
        self.rect = self.image.get_rect(center=old_center)

    def _check_growth_stage(self):
        """成长阶段检测"""
        stages = [60, 120, 180]
        new_stage = sum(1 for threshold in stages if self.size > threshold)
        if new_stage != self.growth_stage:
            self._unlock_ability(new_stage)
            self.growth_stage = new_stage

    def _unlock_ability(self, stage):
        """阶段能力解锁"""
        abilities = [
            "涡流冲击",
            "嗜血狂暴",
            "深海咆哮",
            "名扬天下"
        ]
        print(f"解锁新能力: {abilities[stage]}")
