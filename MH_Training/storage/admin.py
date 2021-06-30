from django.contrib import admin
from .models import Item, ItemType, ItemGroup


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_stock', 'item_image')


class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('item_type_name', 'item_type_sort_priority')


class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('item_group_name', 'item_group_sort_priority')


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ItemGroup, ItemGroupAdmin)
