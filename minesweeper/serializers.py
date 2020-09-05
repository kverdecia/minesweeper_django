from rest_framework.serializers import ModelSerializer

from . import models


class BoardTemplateSerializer(ModelSerializer):
    class Meta:
        model = models.BoardTemplate
        fields = ('id', 'rows', 'columns', 'mines')


class BoardSerializer(ModelSerializer):
    class Meta:
        model = models.Board
        fields = (
            'id', 'rows', 'columns', 'mines', 'board_json', 'finished',
            'user', 'created', 'modified'
        )
