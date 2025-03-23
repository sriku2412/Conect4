import pygame
import sys 

pygame.init()

from app import init_display, draw_frame
from engine import GameEngine
from sounds import load_all_sounds

if __name__ == "__main__":
    pygame.init()
    screen = init_display()
    sounds = load_all_sounds()

    engine = GameEngine(screen, sounds)
    engine.run()

    pygame.quit()