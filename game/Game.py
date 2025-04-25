import pygame
import random
from config.Pixel import pixel_x, pixel_y

from character.FishPlayer import FishPlayer as fp
from character.FishComputer import FishComputer as fc


class Game:
    def __init__(self, species, rect_player, rect_computer, ):
        pygame.init()
        self.screen = pygame.display.set_mode((pixel_x, pixel_y))
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_fish = pygame.sprite.Group()
        self.player_fish = fp(specie=species['1'], rect=rect_player)
        self.game_over = False
        self.victory = False
        self.all_fish.add(self.player_fish)
        self.min_computer_fish = 5  # 电脑鱼最小数量阈值
        '''
        for r in rect_computer:
            # 根据模板生成随机属性
            size = random.randint(species['2']['size_range'][0], species['2']['size_range'][1])
            speed = random.randint(species['2']['speed_range'][0], species['2']['speed_range'][1])
            specie_com = {
                'name': species['2']['name'],
                'size': size,
                'weight': size * species['2']['weight_factor'],  # 重量与大小成正比
                'speed': speed
            }
            small_fish = fc(specie=specie_com, rect=r)
            self.all_fish.add(small_fish)
        '''

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
            return # 同时触发游戏结束
        # update all fish
        keys = pygame.key.get_pressed()
        self.all_fish.update(keys)

        fishes_to_kill = [
            fish for fish in self.all_fish
            if isinstance(fish, fc) and fish.is_out_of_bounds
        ]

        # Detecting collisions
        for fish in self.all_fish:
            if fish != self.player_fish and pygame.sprite.collide_rect(fish, self.player_fish):
                if fish.size > self.player_fish.size:
                    # 玩家受到伤害（逻辑封装在FishPlayer中）
                    self.player_fish.take_damage()
                    '''
                    if self.player_fish.lives <= 0:
                        self.game_over = True
                    '''
                elif self.player_fish.size > fish.size:
                    self.player_fish.eat(fish)
                if fish.weight <= 0:
                    fishes_to_kill.append(fish)
            # 移除被吃掉的鱼
        for fish in fishes_to_kill:
            fish.kill()
        self.spawn_computer_fish_if_needed()

    def spawn_computer_fish_if_needed(self):
        # 统计当前电脑鱼数量
        current_computer = len([fish for fish in self.all_fish if isinstance(fish, fc)])
        # 如果数量不足，补充到至少5条
        while current_computer < self.min_computer_fish:
            self._create_computer_fish_from_edge()
            current_computer += 1

    def _create_computer_fish_from_edge(self):
        # 随机选择一个屏幕边缘方向（0:上，1:下，2:左，3:右）
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

        # 生成属性（根据模板随机生成）
        size = random.randint(20, 40)
        speed = random.randint(1, 3)
        specie_com = {
            'name': 'com',
            'size': size,
            'weight': size * 1,
            'speed': speed
        }
        # 创建带方向的电脑鱼
        new_fish = fc(
            specie=specie_com,
            rect=[x, y],
            direction_x=dir_x,
            direction_y=dir_y
        )
        self.all_fish.add(new_fish)

    def draw(self):
        # draw background and fish
        self.screen.fill('white')
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

        # 显示Game Over
        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render('GAME OVER', True, 'red')
            text_rect = game_over_text.get_rect(center=(pixel_x / 2, pixel_y / 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()


if __name__ == '__main__':
    species = {
        '1': {
            'name': 'gold fish',
            'size': 20,
            'weight': 20,
            'speed': 5,
        },
        '2': {  # 电脑鱼（随机属性模板）
            'name': 'com',
            'size_range': [10, 50],  # 大小范围
            'weight_factor': 1,  # 重量 = size * factor
            'speed_range': [1, 3]  # 速度范围
        }
    }
    rect_player = [pixel_x / 2, pixel_y / 2]
    rect_computer = []
    for i in range(3):
        rect_computer.append([random.randint(0, pixel_x), random.randint(0, pixel_y)])
