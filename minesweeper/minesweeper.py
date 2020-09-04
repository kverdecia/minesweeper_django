from typing import Set, Tuple, Iterator, List, Optional
import random
import enum


class CellType(enum.IntEnum):
    EMPTY = 0
    BOMB = 1
    FLAG = 2
    QUESTION = 4


class Board:
    "Mine sweeper board logic"

    rows: int
    columns: int
    mines: int
    board: List[List[Optional[int]]]

    def __init__(self, rows: int, columns: int, mines: int):
        """
        Initialize a mine sweeper board. Mines are randomly placed.

        Parameters
        ----------
        rows: int
            Count of rows of the board.
        cols: int
            Count of columns of the board.
        mines: int
            Count of mines to places on the board.
        """
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.board = [[CellType.EMPTY]*columns for i in range(rows)]
        for row, col in self._random_cells():
            self.board[row][col] = CellType.BOMB

    def _random_cell(self, omit: Set[Tuple[int, int]]) -> Tuple[int, int]:
        """Returns a random cell coordinate that is not in in `omit`
        
        Parameters
        ----------
        omit: Set[Tuple[int, int]]
            Set of random cells that cannot be returned by this method.
        
        Retuns
        ------
        result: Tuple[int, int]
            Returns a random cell.
        
        Raises
        ------
        ValueError:
            If there are more cell in the `omit` set than the third of cells in the board.
        """
        if len(omit) >= self.rows * self.columns / 3:
            raise ValueError("the omit set if full of mines.")
        result = (random.randint(0, self.rows-1), random.randint(0, self.columns-1))
        while result in omit:
            result = (random.randint(0, self.rows-1), random.randint(0, self.columns-1))

        return result

    def _random_cells(self) -> Iterator[Tuple[int, int]]:
        "Returns an iterator of unique `self.mines` random cells."
        omit: Set[Tuple[int, int]] = set()
        for i in range(self.mines):
            cell = self._random_cell(omit)
            omit.add(cell)
            yield cell
