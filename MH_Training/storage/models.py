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
    type_item = models.ForeignKey(ItemType, related_name='type_item', on_delete=models.CASCADE)
    group_item = models.ManyToManyField(ItemGroup, related_name='group')

    def __str__(self):
        return self.name_item


class Storage(models.Model):

    name_storage = models.CharField(max_length=200)

    def __str__(self):
        return self.name_storage


class ItemContainer(models.Model):

    item_container = models.ForeignKey(Item, related_name='item_container', on_delete=models.CASCADE)
    amount_container = models.IntegerField()
    storage_container = models.ForeignKey(Storage, related_name='storage_container', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item_container) + ' on ' + str(self.storage_container)


class EventType(models.Model):

    name_eventtype = models.CharField(max_length=200)

    def __str__(self):
        return self.name_eventtype


class Event(models.Model):

    name_event = models.CharField(max_length=200)
    date_event = models.DateField()
    type_event = models.ForeignKey(EventType, related_name='type_event', on_delete=models.CASCADE)

    def __str__(self):
        return self.name_event


class ItemRequest(models.Model):
    STATUS_VARS = (
        ('TD', 'ToDo'),
        ('IP', 'InProgress'),
        ('D', 'Done'),
        ('UD', 'UnDone')
    )

    item_request = models.ForeignKey(Item, related_name='item_request', on_delete=models.CASCADE)
    amount_itemrequest = models.IntegerField()
    event_itemrequest = models.ForeignKey(Event, related_name='event_itemrequest', on_delete=models.CASCADE)
    storage_out = models.ForeignKey(Storage, related_name='storage_out', on_delete=models.CASCADE)
    storage_in = models.ForeignKey(Storage, related_name='storage_in', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_VARS)

    def __str__(self):
        return str(self.amount_itemrequest) + '(' + str(self.item_request) + ') ' \
               + str(self.storage_out) + ' to ' + str(self.storage_in)
