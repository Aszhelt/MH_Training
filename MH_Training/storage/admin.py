from django.contrib import admin

from .models import ItemGroup, Item, \
    ItemRequest, ItemContainer, Storage, Order


class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('name_item_group', 'sort_priority_item_group',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name_item',)


class StorageAdmin(admin.ModelAdmin):
    list_display = ('name_storage', 'user_storage', 'is_public', 'group_storage')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_order', 'user_order', 'storage_from', 'storage_to', 'status_order')


class ItemContainerAdmin(admin.ModelAdmin):
    list_display = ('item_in_container', 'amount_in_container', 'storage_container')


class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ('item_in_request', 'amount_in_request', 'status_item_request', 'order_request')


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemGroup, ItemGroupAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemContainer, ItemContainerAdmin)
admin.site.register(ItemRequest, ItemRequestAdmin)
