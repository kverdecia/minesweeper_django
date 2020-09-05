from django.db.models import query

from rest_framework.serializers import ModelSerializer
from rest_framework import generics

from . import models
from . import serializers


class ListBoardTemplateView(generics.ListAPIView):
    serializer_class = serializers.BoardTemplateSerializer
    queryset = models.BoardTemplate.objects.all()


class ListCreateBoardView(generics.ListCreateAPIView):
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return models.Board.objects.filter(user=self.request.user)

    def perform_create(self, serializer: ModelSerializer):
        serializer.save(user=self.request.user)


class ReadDeleteBoardView(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return models.Board.objects.filter(user=self.request.user)
