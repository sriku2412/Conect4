
import pygame
import logging

logger = logging.getLogger(__name__)


def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        logger.error(f"Failed to load sound: {path} | Error: {e}")
        return None


def load_all_sounds():
    return {
        "drop": load_sound("utils/sound/drop.wav"),
        "win": load_sound("utils/sound/win.wav"),
        "draw": load_sound("utils/sound/draw.wav"),
        "start": load_sound("utils/sound/start.wav")
    }


