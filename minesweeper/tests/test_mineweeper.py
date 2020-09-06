#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase

from .. import minesweeper
from ..minesweeper import CellType


class TestMineSweeper(TestCase):
    def setUp(self):
        self.full_board = minesweeper.Board(3, 3, 1)
        BOMB = minesweeper.CellType.BOMB
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

