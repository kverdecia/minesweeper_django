from re import U
from django.utils.translation import ugettext_lazy as _
from django.db.models import TextChoices

from rest_framework import serializers

from . import models


class BoardTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BoardTemplate
        fields = ('id', 'rows', 'columns', 'mines')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = (
            'id', 'rows', 'columns', 'mines', 'board_json', 'finished',
            'user', 'created', 'modified'
        )


class UpdateCellOperation(TextChoices):
    MARK_CELL = 'mark_cell', _("Mark cell")
    REVEAL_CELL = 'reveal_cell', _("Reveal cell")


class UpdateCellSerializer(serializers.Serializer):
    row = serializers.IntegerField(write_only=True)
    column = serializers.IntegerField(write_only=True)
    operation = serializers.ChoiceField(write_only=True, choices=UpdateCellOperation.choices)

    class Meta:
        model = models.Board
        fields = (
            'id', 'rows', 'columns', 'mines', 'board_json', 'finished',
            'user', 'created', 'modified'
            'row', 'column', 'operation',
        )
        read_only_fields = (
            'id', 'rows', 'columns', 'mines', 'board_json', 'finished',
            'user', 'created', 'modified'
        )

    def update(self, instance: models.Board, validated_data):
        if validated_data['operation'] == UpdateCellOperation.MARK_CELL:
            instance.mark_cell(validated_data['row'], validated_data['column'])
        elif validated_data['operation'] == UpdateCellOperation.REVEAL_CELL:
            instance.reveal_cell(validated_data['row'], validated_data['column'])
        self._data = BoardSerializer(instance).data
        return instance
