from django.contrib import admin
from .models import Item, Tag, GroupTag


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'image')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GroupTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(Item, ItemAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(GroupTag, GroupTagAdmin)
