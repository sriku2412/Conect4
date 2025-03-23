# utils/game_engine.py:
import numpy as np
from pydantic import BaseModel
from utils.config import ROW_COUNT, COLUMN_COUNT, WIN_COUNT

class Board(BaseModel):
    grid: np.ndarray

    model_config = {
        "arbitrary_types_allowed": True
    }

    @classmethod
    def create(cls):
        return cls(grid=np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int))

    def is_valid_location(self, col: int) -> bool:
        if 0 <= col < COLUMN_COUNT:
            return self.grid[ROW_COUNT - 1][col] == 0
        return False  # prevent out-of-bound errors

    def get_next_open_row(self, col: int) -> int:
        for r in range(ROW_COUNT):
            if self.grid[r][col] == 0:
                return r
        raise ValueError("Column is full")

    def drop_piece(self, row: int, col: int, piece: int):
        self.grid[row][col] = piece

    def winning_move(self, piece: int) -> list[tuple[int, int]] | None:
        b = self.grid

        # Horizontal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if all(b[r][c + i] == piece for i in range(WIN_COUNT)):
                    return [(r, c + i) for i in range(WIN_COUNT)]

        # Vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if all(b[r + i][c] == piece for i in range(WIN_COUNT)):
                    return [(r + i, c) for i in range(WIN_COUNT)]

        # Positive Diagonal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if all(b[r + i][c + i] == piece for i in range(WIN_COUNT)):
                    return [(r + i, c + i) for i in range(WIN_COUNT)]

        # Negative Diagonal
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if all(b[r - i][c + i] == piece for i in range(WIN_COUNT)):
                    return [(r - i, c + i) for i in range(WIN_COUNT)]

        return None

    def is_full(self) -> bool:
        return not any(self.is_valid_location(c) for c in range(COLUMN_COUNT))
