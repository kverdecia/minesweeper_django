from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from . import minesweeper


class BoardSize(models.Model):
    rows = models.PositiveIntegerField(_("Rows"))
    columns = models.PositiveIntegerField(_("Columns"))
    mines = models.PositiveIntegerField(_("Mines"))

    class Meta:
        abstract = True

class BoardTemplate(BoardSize):
    class Meta:
        unique_together = [('rows', 'columns', 'mines')]
        verbose_name = _("Board template")
        verbose_name_plural = _("Board templates")
        ordering = ['rows', 'columns', 'mines']


class Board(BoardSize):
    board_json = models.JSONField(verbose_name=_("Board JSON"), editable=False)
    finished = models.BooleanField(_("Finished"), blank=True, default=False, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='minesweeper_boards', editable=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    class Meta:
        unique_together = [('rows', 'columns', 'mines')]
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")

    def save(self, *args, **kwargs):
        if self.pk is None:
            board = minesweeper.Board(self.rows, self.columns, self.mines)
            self.board_json = board.board
        return super().save(*args, **kwargs)
