from django.db.models import query
from rest_framework import generics

from . import models
from . import serializers


class ListBoardTemplateView(generics.ListAPIView):
    serializer_class = serializers.BoardTemplateSerializer
    queryset = models.BoardTemplate.objects.all()
