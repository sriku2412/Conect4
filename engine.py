import pygame
import random
import sys
import logging
from utils.config import *
from utils.game_engine import Board
from utils.dqn_agent import DQNAgent
from app import draw_frame
from events import handle_player_turn, handle_ai_turn, wait_for_next_game
from ai_logic import get_minimax_move, get_dqn_move

logger = logging.getLogger(__name__)

class GameEngine:
    def __init__(self, screen, sounds):
        self.screen = screen
        self.sounds = sounds
        self.agent = DQNAgent(model_size="large", use_double_dqn=True)
        self.agent.load("utils/dqn_model.pth")
        self.clock = pygame.time.Clock()
        self.starting_turn = random.randint(0, 1)
        self.reset_scores()

    def reset_scores(self):
        self.player_score = 0
        self.ai_score = 0
        self.round_number = 1
        self.starting_turn = random.randint(0, 1)

    def run(self):
        try:
            while True:
                if self.sounds["start"]:
                    pygame.mixer.Sound.play(self.sounds["start"])

                board = Board.create()
                draw_frame(self.screen, board, self.round_number, self.player_score, self.ai_score)

                # Alternate starting player after the first round
                if self.round_number == 1:
                    turn = self.starting_turn
                else:
                    self.starting_turn = 1 - self.starting_turn
                    turn = self.starting_turn

                game_over = False

                while not game_over:
                    draw_frame(self.screen, board, self.round_number, self.player_score, self.ai_score)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.reset_scores()
                                return self.run()
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                        if turn == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                            col = event.pos[0] // SQUARESIZE
                            result = handle_player_turn(
                                board, self.screen, col, self.sounds,
                                self.round_number, self.player_score, self.ai_score
                            )
                            if result:
                                if result == "win":
                                    self.player_score += 1
                                game_over = True
                            turn = 1

                    if turn == 1 and not game_over:
                        result = handle_ai_turn(
                            board, self.screen, lambda b: get_minimax_move(b), self.sounds,
                            self.round_number, self.player_score, self.ai_score
                        )
                        if result:
                            if result == "win":
                                self.ai_score += 1
                            game_over = True
                        turn = 0

                    self.clock.tick(30)

                wait_for_next_game()
                self.round_number += 1

        except Exception as e:
            logger.exception("Unexpected error occurred in game loop")
            pygame.quit()
            sys.exit(1)
