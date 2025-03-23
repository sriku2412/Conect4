import pygame
import sys
from utils.config import *
from app import draw_frame
from utils.game_engine import Board

def wait_for_next_game():
    font = pygame.font.SysFont("monospace", 32)
    label = font.render("Click to start next game", True, GRAY)
    screen_rect = pygame.display.get_surface().get_rect()
    label_rect = label.get_rect(center=(screen_rect.centerx, screen_rect.centery))
    pygame.draw.rect(pygame.display.get_surface(), BLACK, label_rect.inflate(20, 20))
    pygame.display.get_surface().blit(label, label_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def handle_player_turn(board, screen, col, sounds, round_number, player_score, ai_score) -> str | None:
    if board.is_valid_location(col):
        row = board.get_next_open_row(col)
        board.drop_piece(row, col, PLAYER)

        draw_frame(screen, board, round_number, player_score, ai_score)
        pygame.display.update()
        pygame.time.wait(150)

        if sounds["drop"]:
            pygame.mixer.Sound.play(sounds["drop"])

        if win_positions := board.winning_move(PLAYER):
            draw_frame(screen, board, round_number, player_score, ai_score, highlight_positions=win_positions)
            pygame.display.update()
            pygame.time.wait(600)
            _show_message(screen, "You win this round!", RED, sounds["win"])
            return "win"

        elif board.is_full():
            _show_message(screen, "It's a draw!", GRAY, sounds["draw"])
            return "draw"
    return None


def handle_ai_turn(board, screen, ai_move_fn, sounds, round_number, player_score, ai_score) -> str | None:
    col = ai_move_fn(board)
    if board.is_valid_location(col):
        row = board.get_next_open_row(col)
        board.drop_piece(row, col, AI)

        draw_frame(screen, board, round_number, player_score, ai_score)
        pygame.display.update()
        pygame.time.wait(150)

        if sounds["drop"]:
            pygame.mixer.Sound.play(sounds["drop"])

        if win_positions := board.winning_move(AI):
            draw_frame(screen, board, round_number, player_score, ai_score, highlight_positions=win_positions)
            pygame.display.update()
            pygame.time.wait(600)
            _show_message(screen, "AI wins this round!", YELLOW, sounds["win"])
            return "win"

        elif board.is_full():
            _show_message(screen, "It's a draw!", GRAY, sounds["draw"])
            return "draw"
    return None


def _show_message(screen, message, color, sound):
    font = pygame.font.SysFont("monospace", 50)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
    label = font.render(message, 1, color)
    label_rect = label.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
    screen.blit(label, label_rect)
    pygame.display.update()
    if sound:
        pygame.mixer.Sound.play(sound)
