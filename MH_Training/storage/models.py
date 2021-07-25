from django.db import models
from django.contrib.auth.models import User, Group


class ItemGroup(models.Model):
    name_item_group = models.CharField(max_length=100, unique=True)
    image_item_group = models.ImageField(upload_to='storage/item_group/')
    sort_priority_item_group = models.IntegerField()

    def __str__(self):
        return self.name_item_group


class Item(models.Model):
    name_item = models.CharField(max_length=100, unique=True)
    group_item = models.ForeignKey(ItemGroup, related_name='group_item',
                                   on_delete=models.SET_NULL, blank=True, null=True)
    image_item = models.ImageField(upload_to='storage/item')

    def __str__(self):
        return self.name_item


class Storage(models.Model):
    name_storage = models.CharField(max_length=100, unique=True)
    user_storage = models.ForeignKey(User, related_name='user_storage', on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    is_temporary = models.BooleanField(default=False)
    group_storage = models.ForeignKey(Group, related_name='group_storage',
                                      on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_storage


class ItemContainer(models.Model):
    item_in_container = models.ForeignKey(Item, related_name='item_in_container', on_delete=models.CASCADE)
    amount_in_container = models.PositiveIntegerField()
    storage_container = models.ForeignKey(Storage, related_name='storage_container', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.amount_in_container}({self.item_in_container}) on {self.storage_container} storage'


class Order(models.Model):
    STATUS_VARS = (
        ('Recipient', (
                ('DR', 'Draft'),
                ('TD', 'To Do'),
                ('DN', 'Done'),
                ('СR', 'Canceled by Recipient'),
                ('L', 'Lost'),
            )
         ),
        ('Sender', (
                ('IP', 'In Progress'),
                ('IR', 'In Road'),
                ('CS', 'Canceled by Sender'),
            )
         ),
        ('Creator', (
                ('CC', 'Canceled by Creator'),
            )
         ),
    )

    date_order = models.DateField()
    user_order = models.ForeignKey(User, related_name='user_order', on_delete=models.CASCADE)
    storage_from = models.ForeignKey(Storage, related_name='storage_from', on_delete=models.CASCADE)
    storage_to = models.ForeignKey(Storage, related_name='storage_to', on_delete=models.CASCADE)
    status_order = models.CharField(max_length=2, choices=STATUS_VARS, default='DR')

    def __str__(self):
        return f'{self.user_order} order on {self.date_order} ' \
               f'from {self.storage_from} to {self.storage_to}'


class ItemRequest(models.Model):
    STATUS_VARS = (
        ('ND', 'Not Done'),
        ('IP', 'In Progress'),
        ('D', 'Done'),
        ('L', 'Lost'),
    )

    item_in_request = models.ForeignKey(Item, related_name='item_in_request', on_delete=models.CASCADE)
    amount_in_request = models.PositiveIntegerField()
    order_request = models.ForeignKey(Order, related_name='order_request',
                                      on_delete=models.CASCADE)
    status_item_request = models.CharField(max_length=2, choices=STATUS_VARS, default='ND')

    def __str__(self):
        return f'{self.amount_in_request}({self.item_in_request}) ' \
               f'{self.order_request} request_status ({self.status_item_request})'
