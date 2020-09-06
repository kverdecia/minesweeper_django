from django.utils.translation import ugettext_lazy as _

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


class UpdateCellSerializer(serializers.Serializer):
    row = serializers.IntegerField(write_only=True)
    column = serializers.IntegerField(write_only=True)
    operation = serializers.ChoiceField(write_only=True, choices=[
        ('mark_cell', _("Mark cell")),
    ])

    class Meta:
        model = models.Board
        fields = (
            'row', 'column', 'operation',
        )

    def update(self, instance: models.Board, validated_data):
        instance.mark_cell(validated_data['row'], validated_data['column'])
        return instance
