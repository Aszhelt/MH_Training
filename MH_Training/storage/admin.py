from django.contrib import admin
from .models import ItemType, ItemGroup, Item, Storage, Container


class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name_itemtype',)


class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('name_itemgroup',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name_item',)


class StorageAdmin(admin.ModelAdmin):
    list_display = ('name_storage',)


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('item', 'storage', 'amount')


admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ItemGroup, ItemGroupAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Container, ContainerAdmin)
