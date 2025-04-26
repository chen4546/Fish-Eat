import pygame
import gettext
from game.Game import Game
import random
from config.config import pixel_x,pixel_y
from config.player import SPECIES
from config.computer import STAGE_WEIGHTS,FISH_CLASSES
def main():
    species=SPECIES
    stage_weights=STAGE_WEIGHTS
    fish_types=FISH_CLASSES
    rect_player = [pixel_x/2, pixel_y/2]
    rect_computer = []
    for i in range(0):
        rect_computer.append([random.randint(0, pixel_x), random.randint(0, pixel_y)])

    game = Game(
        species=species,
        computer_fish_types=fish_types,
        rect_player=rect_player,
        rect_computer=rect_computer,
        stage_weights=stage_weights
    )

    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
