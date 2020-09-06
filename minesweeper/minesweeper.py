
import itertools
from typing import Callable, Optional, Set, Tuple, Iterator, List, Any, Union, Iterable
import random
import enum


class CellType(enum.IntEnum):
    EMPTY = 0
    BOMB = 1
    FLAG = 2
    QUESTION = 4
    REVEALED = 8
    KABOOM = 16


class CellOperation(enum.Enum):
    REVEAL = 0
    FLAG = 2
    QUESTION = 4


class MineExplossionError(Exception):
    pass


class Board:
    "Mine sweeper board logic"

    rows: int
    columns: int
    mines: int
    board: List[List[CellType]]

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
        if not rows:
            raise ValueError("row count cannot be empty")
        if not columns:
            raise ValueError("column count cannot be empty")
        if not mines:
            raise ValueError("mines count must not be empty")
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.board = [[CellType.EMPTY]*columns for i in range(rows)]
        for row, col in self._random_cells():
            self.board[row][col] = CellType.BOMB

    def __getitem__(self, cell_pos: Tuple[int, int]) -> CellType:
        col, row = cell_pos
        return self.board[row][col]

    def __setitem__(self, cell_pos: Tuple[int, int], value: Union[int, CellType]):
        col, row = cell_pos
        self.board[row][col] = value # type: ignore

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

    def is_type(self, row: int, column: int, cell_type: Any) -> bool:
        return bool(self[row, column] & cell_type)

    def is_empty(self, row: int, column: int) -> bool:
        "Returns if the cell is empty"
        return self[row, column] == CellType.EMPTY

    def add_type(self, row: int, column: int, cell_type: Any):
        self[row, column] = self[row, column] | cell_type

    def delete_type(self, row: int, column: int, cell_type: Any):
        self[row, column] = (self[row, column] | cell_type ) ^ cell_type

    def mark_cell(self, row: int, column: int):
        if self.is_type(row, column, CellType.QUESTION):
            self.delete_type(row, column, CellType.QUESTION)
        elif self.is_type(row, column, CellType.FLAG):
            self.delete_type(row, column, CellType.FLAG)
            self.add_type(row, column, CellType.QUESTION)
        else:
            self.add_type(row, column, CellType.FLAG)

    def is_marked(self, row: int, column: int) -> bool:
        return self.is_type(row, column, CellType.FLAG) or self.is_type(row, column, CellType.QUESTION)
