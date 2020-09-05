#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase

from .. import minesweeper


class TestMineSweeper(TestCase):
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
