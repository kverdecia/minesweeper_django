import pprint

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from . import models


@admin.register(models.BoardTemplate)
class BoardTemplateAdmin(admin.ModelAdmin):
    list_display = ('rows', 'columns', 'mines')


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('rows', 'columns', 'mines', 'finished', 'user', 'created', 'modified')
    fields = ('rows', 'columns', 'mines', 'get_board_json', 'finished', 'user', 'created', 'modified')
    readonly_fields = ('get_board_json', 'finished', 'user', 'created', 'modified')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_board_json(self, obj):
        return pprint.pformat(obj.board_json, indent=4, width=400)
    get_board_json.short_description = _("Board JSON")
