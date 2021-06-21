from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV

from .models import Item, Bid


class CustomImportExportModelAdmin(ImportExportModelAdmin):
  formats = [CSV]


@admin.register(Item)
class ItemAdmin(CustomImportExportModelAdmin):
  pass


admin.site.register(Bid)