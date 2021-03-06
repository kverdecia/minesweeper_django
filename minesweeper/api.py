from django.db.models import query
from django.utils.decorators import method_decorator
from requests.api import put

from rest_framework.serializers import ModelSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication as BaseSessionAuthentication, BasicAuthentication

from drf_yasg.utils import swagger_auto_schema

from . import models
from . import serializers


class SessionAuthentication(BaseSessionAuthentication):
    def enforce_csrf(self, request):
        return


class ListBoardTemplateView(generics.ListAPIView):
    serializer_class = serializers.BoardTemplateSerializer
    queryset = models.BoardTemplate.objects.all()


class ListCreateBoardView(generics.ListCreateAPIView):
    serializer_class = serializers.BoardSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return models.Board.objects.filter(user=self.request.user)

    def perform_create(self, serializer: ModelSerializer):
        serializer.save(user=self.request.user)


class ReadUpdateDeleteBoardView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return models.Board.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return serializers.UpdateCellSerializer
        return serializers.BoardSerializer

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: serializers.BoardSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)