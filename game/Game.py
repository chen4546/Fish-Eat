import pygame
import random
from config.config import pixel_x, pixel_y,fish_computer

from character.FishPlayer import FishPlayer as fp
from character.FishComputer import FishComputer as fc
from config.sound import EAT,HURT,WY


class Game:
    def __init__(self, species, rect_player, computer_fish_types, stage_weights, rect_computer=None, ):

        pygame.init()
        # 初始化时加载音效
        self.eat_sound = pygame.mixer.Sound(random.choice(EAT))
        self.hurt_sound = pygame.mixer.Sound(random.choice(HURT))
        self.wy=[pygame.mixer.Sound(random.choice(WY['hurt'])),
                 pygame.mixer.Sound(random.choice(WY['eat'])),
                 pygame.mixer.Sound(random.choice(WY['fail'])),
                 pygame.mixer.Sound(random.choice(WY['win'])),
                 pygame.mixer.Sound(random.choice(WY['win_half'])),]
        self.screen = pygame.display.set_mode((pixel_x, pixel_y))
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_fish = pygame.sprite.Group()
        self.player_fish = fp(specie=species['1'], rect=rect_player)
        self.fish_types = computer_fish_types
        self.stage_weights = stage_weights
        self.game_over = False
        self.victory = False
        self.all_fish.add(self.player_fish)
        self.min_computer_fish = fish_computer  # 电脑鱼最小数量阈值
        self.win_play=False
        self.half_win_play = False
        self.fail_play = False
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        # exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        if self.player_fish.lives <= 0:
            self.game_over = True
            return
        if self.player_fish.win:
            self.game_over = True
            return  # 同时触发游戏结束
        # update all fish
        keys = pygame.key.get_pressed()
        self.all_fish.update(keys)

        fishes_to_kill = [
            fish for fish in self.all_fish
            if isinstance(fish, fc) and fish.is_out_of_bounds
        ]

        # Detecting collisions
        for fish in self.all_fish:
            # 在Game类的update方法中修改碰撞检测逻辑
            if fish != self.player_fish and self.player_fish.check_collision(fish):
                if fish.size > self.player_fish.size:
                    # 玩家受到伤害（逻辑封装在FishPlayer中）
                    if self.player_fish.take_damage():
                        #self.hurt_sound.play()
                        self.wy[0].play()
                    '''
                    if self.player_fish.lives <= 0:
                        self.game_over = True
                    '''
                elif self.player_fish.size > fish.size:
                    self.player_fish.eat(fish)
                    #self.eat_sound.play()
                    self.wy[1].play()
                if fish.weight <= 0:
                    fishes_to_kill.append(fish)
            # 移除被吃掉的鱼
        for fish in fishes_to_kill:
            fish.kill()
            # 检查是否有比玩家大或小的鱼
        has_larger = any(fish.size > self.player_fish.size for fish in self.all_fish if fish != self.player_fish)
        has_smaller = any(fish.size < self.player_fish.size for fish in self.all_fish if fish != self.player_fish)
        self.spawn_computer_fish_if_needed()

    def spawn_computer_fish_if_needed(self):
        # 统计当前电脑鱼数量
        current_computer = len([fish for fish in self.all_fish if isinstance(fish, fc)])
        # print(current_computer)
        # 如果数量不足，补充到至少5条
        while current_computer < self.min_computer_fish:
            self._create_computer_fish_from_edge()
            current_computer += 1

    # 在Game类的spawn_computer_fish_if_needed方法中修改
    def _create_computer_fish_from_edge(self, fish_type=None, size=None, speed=None):
        if fish_type is not None:
            self._create_specific_fish(fish_type, size, speed)
        else:
            pass
        x, y, dir_x, dir_y = self.random_position()
        # 选择鱼类类别
        stage=min(self.player_fish.growth_stage,3)
        class_names = ['small', 'medium', 'large', 'special']
        class_weights=self.stage_weights['class_weights'][stage]
        selected_class = random.choices(class_names, weights=class_weights, k=1)[0]

        # 选择具体鱼类
        fish_group = self.fish_types[selected_class]
        inner_weights = self.stage_weights['inner_weights'][selected_class]
        selected_type = random.choices(fish_group, weights=inner_weights, k=1)[0]

        # 生成属性
        size = random.randint(*selected_type['size_range'])
        speed = random.randint(*selected_type['speed_range'])
        specie_com = {
            'name': selected_type['name'],
            'size': size,
            'weight': size * 1,
            'speed': speed,
        }

        # 创建带方向的电脑鱼
        new_fish = fc(
            game=self,
            specie=specie_com,
            rect=[x, y],
            direction_x=dir_x,
            direction_y=dir_y
        )
        self.all_fish.add(new_fish)

    def random_position(self):
        edge = random.randint(0, 3)
        if edge == 0:  # 上方进入
            x = random.randint(0, pixel_x)
            y = -20  # 从屏幕外上方进入
            dir_x, dir_y = 0, 1  # 向下移动
        elif edge == 1:  # 下方进入
            x = random.randint(0, pixel_x)
            y = pixel_y + 20  # 从屏幕外下方进入
            dir_x, dir_y = 0, -1  # 向上移动
        elif edge == 2:  # 左侧进入
            x = -20  # 从屏幕外左侧进入
            y = random.randint(0, pixel_y)
            dir_x, dir_y = 1, 0  # 向右移动
        else:  # 右侧进入
            x = pixel_x + 20  # 从屏幕外右侧进入
            y = random.randint(0, pixel_y)
            dir_x, dir_y = -1, 0  # 向左移动
        return x, y, dir_x, dir_y

    def draw(self):
        # draw background and fish
        bg_image_path="drawable/background/background.jpg"
        background=pygame.image.load(bg_image_path)
        #self.screen.fill('white')
        self.screen.blit(background,(0,0))
        self._draw_status_bar()
        # 调试信息
        # if self.DEBUG_MODE:
        #     self._draw_debug_info()
        # 绘制所有鱼
        for fish in self.all_fish:
            if fish == self.player_fish:
                fish.draw(self.screen)  # 直接调用玩家鱼的draw方法
            else:
                self.screen.blit(fish.image, fish.rect)

        # 显示剩余生命
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f'Lives: {self.player_fish.lives}', True, 'black')
        self.screen.blit(lives_text, (10, 10))
        # 在Game的draw方法中显示分数
        score_text = font.render(f'Score: {self.player_fish.score}', True, 'black')
        self.screen.blit(score_text, (10, 50))

        # 显示Game Over
        if self.game_over and not self.fail_play:
            self.wy[2].play()
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render('GAME OVER', True, 'red')
            text_rect = game_over_text.get_rect(center=(pixel_x / 2, pixel_y / 2))
            self.screen.blit(game_over_text, text_rect)
        # 显示win
        if self.player_fish.win and not self.win_play:
            self.wy[3].play()
            win_font = pygame.font.Font(None, 72)
            win_text = win_font.render('WIN', True, 'green')
            text_rect = win_text.get_rect(center=(pixel_x / 2, pixel_y / 2))
            self.screen.blit(win_text, text_rect)
            self.win_play=True
        if self.player_fish.score>10 and not self.half_win_play:
            self.wy[4].play()
            self.half_win_play=True

        pygame.display.flip()


    def _draw_status_bar(self):
        """绘制玩家状态栏"""
        # 生命值
        life_width = 200
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, life_width, 20))
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (10, 10, life_width * (self.player_fish.lives / self.player_fish.max_lives), 20))

        # 耐力条
        stamina_height = 15
        pygame.draw.rect(self.screen, (100, 100, 255),
                         (pixel_x - 120, 10, 20, 100))
        pygame.draw.rect(self.screen, (0, 200, 255),
                         (pixel_x - 120, 10 + (100 - self.player_fish.stamina),
                          20, self.player_fish.stamina))

        # 阶段显示
        stage_names = ["幼鱼期", "成长期", "成熟期", "海洋霸主"]
        font = pygame.font.Font(None, 24)
        text = font.render(f"阶段: {stage_names[self.player_fish.growth_stage]}", True, (0, 0, 0))
        self.screen.blit(text, (pixel_x - 200, 10))


    def _draw_debug_info(self):
        """调试信息显示"""
        debug_text = [
            f"体型: {self.player_fish.size:.1f}",
            f"实际速度: {self.player_fish.current_speed:.1f}",
            f"攻击系数: {self.player_fish.attack_ratio:.1f}x",
            f"生命恢复: {self.player_fish.regen_rate:.1f}/s"
        ]
        y_pos = 100
        for text in debug_text:
            surface = self.debug_font.render(text, True, (0, 0, 0))
            self.screen.blit(surface, (10, y_pos))
            y_pos += 25
