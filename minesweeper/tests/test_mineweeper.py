#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

from django.test import TestCase

from .. import minesweeper
from ..minesweeper import CellType


BOMB = CellType.BOMB
REVEALED = CellType.REVEALED
EMPTY = CellType.EMPTY
FLAG = CellType.FLAG


class TestMineSweeper(TestCase):
    def setUp(self):
        # create a board where all cells have mines.
        self.full_board = minesweeper.Board(3, 3, 1)
        self.full_board.board = [
            [BOMB, BOMB, BOMB],
            [BOMB, BOMB, BOMB],
            [BOMB, BOMB, BOMB],
        ]

    def test_required_parameters_on_create(self):
        self.assertRaises(ValueError, minesweeper.Board, 0, 0, 0)
        self.assertRaises(ValueError, minesweeper.Board, 20, 0, 0)
        self.assertRaises(ValueError, minesweeper.Board, 0, 20, 0)
        self.assertRaises(ValueError, minesweeper.Board, 0, 0, 20)
        self.assertRaises(ValueError, minesweeper.Board, 20, 20, 0)
        self.assertRaises(ValueError, minesweeper.Board, 20, 0, 20)
        self.assertRaises(ValueError, minesweeper.Board, 0, 20, 20)
        
    def test_create_board(self):
        rows = 30
        cols = 40
        mines = 200
        board = minesweeper.Board(rows, cols, mines)
        # test dimensions
        self.assertEqual(board.rows, rows)
        self.assertEqual(board.columns, cols)
        self.assertEqual(board.mines, mines)
        self.assertEqual(len(board.board), rows)
        mines_count = 0
        empty_count = 0
        # test board dimensions
        for board_row in board.board:
            self.assertEqual(len(board_row), cols)
            for cell in board_row:
                if cell == minesweeper.CellType.EMPTY:
                    empty_count += 1
                elif cell == minesweeper.CellType.BOMB:
                    mines_count += 1
        # test right count of placed mines
        self.assertEqual(mines, mines_count)
        # test all other cells are empty
        self.assertEqual(rows*cols-mines, empty_count)

    def test_getitem(self):
        self.full_board.board[1][1] = CellType.FLAG
        self.assertEqual(self.full_board[0, 0], CellType.BOMB)
        self.assertEqual(self.full_board[1, 1], CellType.FLAG)

    def test_setitem(self):
        self.full_board[1, 1] = CellType.FLAG
        self.assertEqual(self.full_board[0, 0], CellType.BOMB)
        self.assertEqual(self.full_board[1, 1], CellType.FLAG)

    def test_is_empty(self):
        self.full_board[1, 1] = CellType.EMPTY
        self.assertFalse(self.full_board.is_empty(0, 0))
        self.assertTrue(self.full_board.is_empty(1, 1))

    def test_is_type(self):
        self.full_board.board[1][1] = CellType.FLAG
        self.full_board.board[2][2] = CellType.BOMB | CellType.FLAG | CellType.QUESTION
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertTrue(self.full_board.is_type(1, 1, CellType.FLAG))
        self.assertTrue(self.full_board.is_type(2, 2, CellType.BOMB))
        self.assertTrue(self.full_board.is_type(2, 2, CellType.FLAG))
        self.assertTrue(self.full_board.is_type(2, 2, CellType.QUESTION))

    def test_add_type(self):
        self.full_board[0, 0] = CellType.EMPTY
        self.full_board.add_type(0, 0, CellType.BOMB)
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.FLAG))
        self.full_board.add_type(0,0, CellType.FLAG)
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.FLAG))

    def test_delete_type(self):
        self.full_board.add_type(0, 0, CellType.BOMB)
        self.full_board.add_type(0, 0, CellType.FLAG)
        self.full_board.add_type(0, 0, CellType.QUESTION)
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.FLAG))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.QUESTION))
        self.full_board.delete_type(0, 0, CellType.BOMB)
        self.assertFalse(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.FLAG))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.QUESTION))
        self.full_board.delete_type(0, 0, CellType.FLAG)
        self.assertFalse(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.FLAG))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.QUESTION))
        self.full_board.delete_type(0, 0, CellType.QUESTION)
        self.assertFalse(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.FLAG))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.QUESTION))

    def test_mark_cell(self):
        self.full_board.mark_cell(0, 0)
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.FLAG))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.QUESTION))
        self.full_board.mark_cell(0, 0)
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.FLAG))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.QUESTION))
        self.full_board.mark_cell(0, 0)
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.FLAG))
        self.assertFalse(self.full_board.is_type(0, 0, CellType.QUESTION))

    def test_is_marked(self):
        self.assertFalse(self.full_board.is_marked(0, 0))
        self.full_board.mark_cell(0, 0) # first set_mark set type to FLAG
        self.assertTrue(self.full_board.is_marked(0, 0))
        self.full_board.mark_cell(0, 0) # second set_mark set type to QUESTION
        self.assertTrue(self.full_board.is_marked(0, 0))
        self.full_board.mark_cell(0, 0) # third set_mark remove mark
        self.assertFalse(self.full_board.is_marked(0, 0))

    def test_adjacent_cells(self):
        cells = self.full_board.adjacent_cells(1, 1)
        self.assertEqual(cells, [
            (0, 0), (0, 1), (0, 2),
            (1, 0),         (1, 2),
            (2, 0), (2, 1), (2, 2)
        ])
        # test with filter
        self.full_board[0, 0] = CellType.EMPTY
        self.full_board[0, 2] = CellType.EMPTY
        self.full_board[2, 0] = CellType.EMPTY
        self.full_board[2, 2] = CellType.EMPTY
        cells = self.full_board.adjacent_cells(1, 1, self.full_board.has_bomb)
        self.assertEqual(cells, [
                    (0, 1),
            (1, 0),         (1, 2),
                    (2, 1), 
        ])

    def test_has_bomb(self):
        self.assertTrue(self.full_board.has_bomb(0, 0))
        self.full_board[0, 0] = CellType.EMPTY
        self.assertFalse(self.full_board.has_bomb(0, 0))

    def test_is_revealed(self):
        self.assertFalse(self.full_board.is_revealed(0, 0))
        self.full_board.add_type(0, 1, CellType.REVEALED)
        self.assertTrue(self.full_board.is_revealed(0, 1))

    def test_adjacent_mines(self):
        # test this board:
        # EMPTY BOMB|FLAG  BOMB
        # EMPTY EMPTY      BOMB
        # BOMB  BOMB       EMPTY
        self.full_board[0, 0] = CellType.EMPTY
        self.full_board.mark_cell(0, 1)
        self.full_board[1, 0] = CellType.EMPTY
        self.full_board[1, 1] = CellType.EMPTY
        self.full_board[2, 2] = CellType.EMPTY

        self.assertEqual(self.full_board.adjacent_mines(0, 0), [(0, 1)])
        self.assertEqual(self.full_board.adjacent_mines(0, 1), [(0, 2), (1, 2)])
        self.assertEqual(self.full_board.adjacent_mines(0, 2), [(0, 1), (1, 2)])
        self.assertEqual(self.full_board.adjacent_mines(1, 0), [(0, 1), (2, 0), (2, 1)])
        self.assertEqual(self.full_board.adjacent_mines(1, 1), [(0, 1), (0, 2), (1, 2), (2, 0), (2, 1)])
        self.assertEqual(self.full_board.adjacent_mines(1, 2), [(0, 1), (0, 2), (2, 1)])
        self.assertEqual(self.full_board.adjacent_mines(2, 0), [(2, 1)])
        self.assertEqual(self.full_board.adjacent_mines(2, 1), [(1, 2), (2, 0)])
        self.assertEqual(self.full_board.adjacent_mines(2, 2), [(1, 2), (2, 1)])

    def test_adjacent_unmarked_mines_count(self):
        # test this board:
        # EMPTY BOMB|FLAG  BOMB
        # EMPTY EMPTY      BOMB
        # BOMB  BOMB       EMPTY
        self.full_board[0, 0] = CellType.EMPTY
        self.full_board.mark_cell(0, 1)
        self.full_board[1, 0] = CellType.EMPTY
        self.full_board[1, 1] = CellType.EMPTY
        self.full_board[2, 2] = CellType.EMPTY

        self.assertEqual(self.full_board.adjacent_unmarked_mines(0, 0), [])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(0, 1), [(0, 2), (1, 2)])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(0, 2), [(1, 2)])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(1, 0), [(2, 0), (2, 1)])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(1, 1), [(0, 2), (1, 2), (2, 0), (2, 1)])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(1, 2), [(0, 2), (2, 1)])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(2, 0), [(2, 1)])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(2, 1), [(1, 2), (2, 0)])
        self.assertEqual(self.full_board.adjacent_unmarked_mines(2, 2), [(1, 2), (2, 1)])

    def test_reveal_non_empty_non_bomb_cell(self):
        self.full_board.add_type(0, 0, CellType.FLAG)
        board = copy.deepcopy(self.full_board.board)
        self.full_board.reveal(0, 0)
        self.assertEqual(self.full_board.board, board)

        self.full_board.add_type(0, 1, CellType.QUESTION)
        board = copy.deepcopy(self.full_board.board)
        self.full_board.reveal(0, 1)
        self.assertEqual(self.full_board.board, board)

        self.full_board.add_type(0, 2, CellType.REVEALED)
        board = copy.deepcopy(self.full_board.board)
        self.full_board.reveal(0, 2)
        self.assertEqual(self.full_board.board, board)

        self.full_board.add_type(1, 0, CellType.KABOOM)
        board = copy.deepcopy(self.full_board.board)
        self.full_board.reveal(1, 0)
        self.assertEqual(self.full_board.board, board)

    def test_reveal_bomb(self):
        self.assertRaises(minesweeper.MineExplossionError, self.full_board.reveal, 0, 0)
        self.assertTrue(self.full_board.is_type(0, 0, CellType.BOMB))
        self.assertTrue(self.full_board.is_type(0, 0, CellType.KABOOM))

    def test_reveal_cell_with_wrong_value(self):
        self.full_board[0, 0] = 64
        self.assertRaises(ValueError, self.full_board.reveal, 0, 0)
        self.assertEqual(self.full_board[0, 0], 64)

    def test_reveal_empty_cell_case_1(self):
        # test this board (0 is empty):
        # EMPTY BOMB  BOMB
        # EMPTY EMPTY BOMB
        # BOMB  BOMB  EMPTY
        self.full_board[0, 0] = CellType.EMPTY
        self.full_board[1, 0] = CellType.EMPTY
        self.full_board[1, 1] = CellType.EMPTY
        self.full_board[2, 2] = CellType.EMPTY
        self.full_board.reveal(0, 0)
        self.assertEqual(self.full_board.board, [
            [REVEALED, BOMB,     BOMB],
            [EMPTY,    EMPTY,    BOMB],
            [BOMB,     BOMB,     EMPTY],
        ])

    def test_reveal_empty_cell_case_2(self):
        # test this board (0 is empty):
        # EMPTY BOMB|FLAG  BOMB
        # EMPTY EMPTY      BOMB
        # BOMB  BOMB       EMPTY
        self.full_board[0, 0] = CellType.EMPTY
        self.full_board[0, 1] = CellType.EMPTY
        self.full_board[1, 0] = CellType.EMPTY
        self.full_board[1, 1] = CellType.EMPTY
        self.full_board[2, 2] = CellType.EMPTY
        self.full_board.reveal(0, 0)
        self.assertEqual(self.full_board.board, [
            [REVEALED, REVEALED, BOMB],
            [REVEALED, REVEALED, BOMB],
            [BOMB,     BOMB,     EMPTY],
        ])

