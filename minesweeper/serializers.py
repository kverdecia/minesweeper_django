from rest_framework.serializers import ModelSerializer

from . import models


class BoardTemplateSerializer(ModelSerializer):
    class Meta:
        model = models.BoardTemplate
        fields = ('rows', 'columns', 'mines')
