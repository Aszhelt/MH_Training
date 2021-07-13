from django.db import models
from django.contrib.auth.models import User


class ItemType(models.Model):

    name_item_type = models.CharField(max_length=200)
    image_item_type = models.ImageField(upload_to='storage/item_type/')
    sort_priority_item_type = models.IntegerField()

    def __str__(self):
        return self.name_item_type


class ItemGroup(models.Model):

    name_item_group = models.CharField(max_length=200)
    image_item_group = models.ImageField(upload_to='storage/item_group/')
    sort_priority_item_group = models.IntegerField()

    def __str__(self):
        return self.name_item_group


class Item(models.Model):

    name_item = models.CharField(max_length=200)
    image_item = models.ImageField(upload_to='storage/item/')
    type_item = models.ForeignKey(ItemType, related_name='type_item', on_delete=models.CASCADE)
    group_item = models.ManyToManyField(ItemGroup, related_name='group')

    def __str__(self):
        return self.name_item


class Storage(models.Model):

    name_storage = models.CharField(max_length=200)
    user_storage = models.ForeignKey(User, related_name='user_storage', on_delete=models.CASCADE)

    def __str__(self):
        return self.name_storage


class ItemContainer(models.Model):

    item_container = models.ForeignKey(Item, related_name='item_container', on_delete=models.CASCADE)
    amount_container = models.IntegerField()
    storage_container = models.ForeignKey(Storage, related_name='storage_container', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item_container) + ' on ' + str(self.storage_container)


class Event(models.Model):

    user_event = models.ForeignKey(User, related_name='user_event', on_delete=models.CASCADE)
    name_event = models.CharField(max_length=200)
    date_event = models.DateField()

    def __str__(self):
        return self.name_event


class ItemRequest(models.Model):
    STATUS_VARS = (
        ('TD', 'ToDo'),
        ('IP', 'InProgress'),
        ('D', 'Done'),
        ('L', 'Lost'),
        ('C', 'Canceled'),
    )# to int

    item_request = models.ForeignKey(Item, related_name='item_request', on_delete=models.CASCADE)
    amount_item_request = models.IntegerField()
    event_item_request = models.ForeignKey(Event, related_name='event_item_request', on_delete=models.CASCADE)
    storage_out = models.ForeignKey(Storage, related_name='storage_out', on_delete=models.CASCADE)
    storage_in = models.ForeignKey(Storage, related_name='storage_in', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_VARS, default='TD')

    def __str__(self):
        return f'{self.amount_item_request}({self.item_request}) from {self.storage_out} to {self.storage_in}'
