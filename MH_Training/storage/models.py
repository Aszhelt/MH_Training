from django.db import models


class ItemType(models.Model):

    name_itemtype = models.CharField(max_length=200)
    image_itemtype = models.ImageField(upload_to='storage/itemtype/')
    sortpriority_itemtype = models.IntegerField()

    def __str__(self):
        return self.name_itemtype


class ItemGroup(models.Model):

    name_itemgroup = models.CharField(max_length=200)
    image_itemgroup = models.ImageField(upload_to='storage/itemgroup/')
    sortpriority_itemgroup = models.IntegerField()

    def __str__(self):
        return self.name_itemgroup


class Item(models.Model):

    name_item = models.CharField(max_length=200)
    image_item = models.ImageField(upload_to='storage/item/')
    type_item = models.ForeignKey(ItemType, related_name='type', on_delete=models.CASCADE)
    group_item = models.ManyToManyField(ItemGroup, related_name='group')

    def __str__(self):
        return self.name_item


class Storage(models.Model):

    name_storage = models.CharField(max_length=200)

    def __str__(self):
        return self.name_storage


class Container(models.Model):

    item = models.ForeignKey(Item, related_name='item', on_delete=models.CASCADE)
    amount = models.IntegerField()
    storage = models.ForeignKey(Storage, related_name='storage', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item) + ' on ' + str(self.storage)
