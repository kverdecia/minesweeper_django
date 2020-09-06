from django.urls import path

from . import api


urlpatterns = [
    path('board-templates/', api.ListBoardTemplateView.as_view()),
    path('boards/', api.ListCreateBoardView.as_view()),
    path('boards/<int:pk>/', api.ReadUpdateDeleteBoardView.as_view())
]
