import pygame
import gettext
from game.Game import Game
import random
from config.Pixel import pixel_x,pixel_y

def main():
    species = {
        '1': {
            'name': 'gold fish',
            'size': 30,
            'weight': 30,
            'speed': 5,
        },
        '2': {  # 电脑鱼（随机属性模板）
            'name': 'com',
            'size_range': [10, 50],  # 大小范围
            'weight_factor': 1,  # 重量 = size * factor
            'speed_range': [1, 3]  # 速度范围
        }
    }
    rect_player = [pixel_x/2, pixel_y/2]
    rect_computer = []
    for i in range(0):
        rect_computer.append([random.randint(0, pixel_x), random.randint(0, pixel_y)])

    game = Game(species=species, rect_player=rect_player, rect_computer=rect_computer)
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
