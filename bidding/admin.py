from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV

from .models import AuctionSetting, AuctionDescriptionBulletPoint, Item, Bid


class CustomImportExportModelAdmin(ImportExportModelAdmin):
  formats = [CSV]


class AuctionDescriptionBulletPointInline(admin.TabularInline):
    model = AuctionDescriptionBulletPoint
    fields = ("text", "loc")


@admin.register(AuctionSetting)
class AuctionSettingAdmin(admin.ModelAdmin):
  inlines = (AuctionDescriptionBulletPointInline,)


@admin.register(Item)
class ItemAdmin(CustomImportExportModelAdmin):
  pass


admin.site.register(Bid)
admin.site.register(AuctionDescriptionBulletPoint)