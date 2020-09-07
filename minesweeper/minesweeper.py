
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
        row, col = cell_pos
        return self.board[row][col]

    def __setitem__(self, cell_pos: Tuple[int, int], value: Union[int, CellType]):
        row, col = cell_pos
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
        if self.is_type(row, column, CellType.REVEALED):
            return
        if self.is_type(row, column, CellType.QUESTION):
            self.delete_type(row, column, CellType.QUESTION)
        elif self.is_type(row, column, CellType.FLAG):
            self.delete_type(row, column, CellType.FLAG)
            self.add_type(row, column, CellType.QUESTION)
        else:
            self.add_type(row, column, CellType.FLAG)

    def is_marked(self, row: int, column: int) -> bool:
        return self.is_type(row, column, CellType.FLAG) or self.is_type(row, column, CellType.QUESTION)

    def has_bomb(self, row: int, column: int) -> bool:
        return self.is_type(row, column, CellType.BOMB)

    def is_revealed(self, row: int, column: int) -> bool:
        return self.is_type(row, column, CellType.REVEALED)

    def adjacent_cells(self, row: int, column: int, filter: Optional[Callable[[int, int], bool]] = None) -> List[Tuple[int, int]]:
        diffs = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1),
        ]
        if filter is None:
            filter = lambda row, column: True
        result = []
        for diff_row, diff_col in diffs:
            check_row = row + diff_row
            check_col = column + diff_col
            if check_row < 0 or check_col < 0 or check_row >= self.rows or check_col >= self.columns:
                continue
            if filter(check_row, check_col):
                result.append((check_row, check_col))
        return result

    def adjacent_mines(self, row: int, column: int) -> List[Tuple[int, int]]:
        "Returns the count of mines around the cell."
        return self.adjacent_cells(row, column, self.has_bomb)

    def adjacent_unmarked_mines(self, row: int, column: int) -> List[Tuple[int, int]]:
        "Returns the count of mines around the cell."
        is_unmarked_bomb = lambda row, column: self.has_bomb(row, column) and not self.is_marked(row, column)
        return self.adjacent_cells(row, column, is_unmarked_bomb)

    def revealable_neighbours(self, row: int, column: int) -> List[Tuple[int, int]]:
        "Return the list of neighbours that can be revealed"
        if not self.adjacent_unmarked_mines(row, column):
            return self.adjacent_cells(row, column, self.is_empty)
        return []

    def reveal(self, row: int, column: int):
        if self.is_type(row, column, CellType.FLAG|CellType.QUESTION|CellType.REVEALED|CellType.KABOOM):
            return
        if self.has_bomb(row, column):
            self.add_type(row, column, CellType.KABOOM)
            self.add_type(row, column, CellType.REVEALED)
            raise MineExplossionError((row, column))
        if not self.is_empty(row, column):
            raise ValueError(f"Wrong cell value in cell {row},{column}")

        processed: Set[Tuple[int, int]] = set()
        queue = [(row, column)]
        while queue:
            cell = queue.pop(0)
            processed.add(cell)

            if self.is_empty(*cell):
                self.add_type(cell_type=CellType.REVEALED, *cell)

                if not self.adjacent_mines(*cell):
                    is_unprocessed = lambda *cell: cell not in processed
                    queue.extend(self.adjacent_cells(filter=is_unprocessed, *cell))

    def get_display_board(self):
        result = []
        for row, row_cells in enumerate(self.board):
            display_row = []
            for col, value in enumerate(row_cells):
                if self.is_type(row, col, CellType.QUESTION):
                    display_row.append('?')
                elif self.is_type(row, col, CellType.FLAG):
                    display_row.append('!')
                elif self.is_type(row, col, CellType.KABOOM):
                    display_row.append('**')
                elif self.is_type(row, col, CellType.REVEALED):
                    if self.is_type(row, col, CellType.KABOOM):
                        display_row.append('**')
                    if self.is_type(row, col, CellType.BOMB):
                        display_row.append('*')
                    else:
                        mines_count = len(self.adjacent_mines(row, col))
                        display_row.append(str(mines_count))
                else:
                    display_row.append(' ')
            result.append(display_row)
        return result
