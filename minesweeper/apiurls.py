from django.urls import path

from . import api


urlpatterns = [
    path('board-templates/', api.ListBoardTemplateView.as_view()),
]
