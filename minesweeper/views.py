from django.template.base import Template
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'minesweeper/index.html'
