from django.contrib import admin

from .models import \
    ItemType, ItemGroup, Item, \
    Storage, ItemContainer, ItemRequest, Event


class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name_item_type',)


class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('name_item_group',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name_item',)


class StorageAdmin(admin.ModelAdmin):
    list_display = ('name_storage',)


class ItemContainerAdmin(admin.ModelAdmin):
    list_display = ('item_container', 'storage_container', 'amount_container')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name_event', 'date_event')


class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ('item_request', 'amount_item_request', 'storage_out', 'storage_in', 'status')


admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ItemGroup, ItemGroupAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(ItemContainer, ItemContainerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ItemRequest, ItemRequestAdmin)
