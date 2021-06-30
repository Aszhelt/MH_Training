from django.db import models


class ItemGroup(models.Model):
    item_group_name = models.CharField(max_length=200)
    item_group_image = models.ImageField(upload_to='storage/groups/')
    item_group_sort_priority = models.IntegerField()

    def __str__(self):
        return self.item_group_name


class ItemType(models.Model):
    item_type_name = models.CharField(max_length=200)
    item_type_image = models.ImageField(upload_to='storage/tags/')
    item_type_sort_priority = models.IntegerField()

    def __str__(self):
        return self.item_type_name


class Item(models.Model):

    item_name = models.CharField(max_length=300, unique=True)
    item_image = models.ImageField(upload_to='storage/items/')
    item_type = models.ForeignKey(ItemType, related_name='tags', on_delete=models.CASCADE)
    item_stock = models.IntegerField()
    item_group = models.ManyToManyField(ItemGroup, related_name='group')

    def __str__(self):
        return self.item_name
