#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from .. import minesweeper
from .. import models

from . import factories


class TestBoardTemplateModel(TestCase):
    def test_required_fields_on_create(self):
        with transaction.atomic():
            self.assertRaises(IntegrityError, models.BoardTemplate.objects.create)
        with transaction.atomic():
            self.assertRaises(IntegrityError, models.BoardTemplate.objects.create, rows=20)
        with transaction.atomic():
            self.assertRaises(IntegrityError, models.BoardTemplate.objects.create, columns=20)
        with transaction.atomic():
            self.assertRaises(IntegrityError, models.BoardTemplate.objects.create, mines=20)
        with transaction.atomic():
            self.assertRaises(IntegrityError, models.BoardTemplate.objects.create, rows=20, columns=30)
        with transaction.atomic():
            self.assertRaises(IntegrityError, models.BoardTemplate.objects.create, rows=20, mines=10)
        with transaction.atomic():
            self.assertRaises(IntegrityError, models.BoardTemplate.objects.create, columns=20, mines=10)

    def test_duplicated_on_create(self):
        models.BoardTemplate.objects.create(rows=20, columns=20, mines=10)
        self.assertRaises(IntegrityError, models.BoardTemplate.objects.create, rows=20, columns=20, mines=10)

    def test_create_ok(self):
        models.BoardTemplate.objects.create(rows=20, columns=20, mines=10)


class TestBoardModel(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()

    def test_required_fields_on_create(self):
        with transaction.atomic():
            self.assertRaises(ValueError, models.Board.objects.create)
        with transaction.atomic():
            self.assertRaises(ValueError, models.Board.objects.create, rows=20)
        with transaction.atomic():
            self.assertRaises(ValueError, models.Board.objects.create, columns=20)
        with transaction.atomic():
            self.assertRaises(ValueError, models.Board.objects.create, mines=20)
        with transaction.atomic():
            self.assertRaises(ValueError, models.Board.objects.create, rows=20, columns=30)
        with transaction.atomic():
            self.assertRaises(ValueError, models.Board.objects.create, rows=20, mines=10)
        with transaction.atomic():
            self.assertRaises(ValueError, models.Board.objects.create, columns=20, mines=10)

    def test_create_board_model(self):
        rows = 30
        cols = 40
        mines = 200
        board_model: models.Board = models.Board.objects.create(rows=rows, columns=cols, mines=mines,
            user=self.user)
        # test dimensions
        self.assertEqual(board_model.rows, rows)
        self.assertEqual(board_model.columns, cols)
        self.assertEqual(board_model.mines, mines)
        self.assertEqual(len(board_model.board_json), rows)
        mines_count = 0
        empty_count = 0
        # test board dimensions
        for board_row in board_model.board_json:
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
