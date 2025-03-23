import pygame
from utils.config import *

font = pygame.font.SysFont("monospace", 75)


def init_display():
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4 with Hybrid AI")
    return screen


def draw_chip(surface, x, y, outer_color, inner_color):
    pygame.draw.circle(surface, outer_color, (x, y), RADIUS)
    pygame.draw.circle(surface, inner_color, (x, y), RADIUS - 10)
    pygame.draw.circle(surface, BLACK, (x, y), RADIUS, 2)

def draw_board(board, screen, highlight_positions=None):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)
            )
            pygame.draw.circle(
                screen,
                DARK_BLUE,
                (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                RADIUS
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            piece = board.grid[r][c]
            x = int(c * SQUARESIZE + SQUARESIZE / 2)
            y = HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)
            if piece == 1:
                if highlight_positions and (r, c) in highlight_positions:
                    pygame.draw.circle(screen, WHITE, (x, y), RADIUS + 5)
                draw_chip(screen, x, y, RED, DARK_RED)
            elif piece == 2:
                if highlight_positions and (r, c) in highlight_positions:
                    pygame.draw.circle(screen, WHITE, (x, y), RADIUS + 5)
                draw_chip(screen, x, y, YELLOW, DARK_YELLOW)

    pygame.display.update()

def draw_header(screen, round_number, player_score, ai_score):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
    font = pygame.font.SysFont("monospace", 28)
    text = f"Round {round_number} | You: {player_score}  AI: {ai_score}"
    label = font.render(text, 1, YELLOW)
    screen.blit(label, (10, 10))


def draw_frame(screen, board, round_number, player_score, ai_score, highlight_positions=None):
    screen.fill(BLACK)
    draw_header(screen, round_number, player_score, ai_score)
    draw_board(board, screen, highlight_positions)
    pygame.display.update()

