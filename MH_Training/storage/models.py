from django.db import models


class GroupTag(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='storage/groups/')
    sort_priority = models.IntegerField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='storage/tags/')
    sort_priority = models.IntegerField()

    def __str__(self):
        return self.name


class Item(models.Model):

    name = models.CharField(max_length=300, unique=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='storage/items/')
    tags = models.ManyToManyField(Tag, related_name='tags')
    group = models.ManyToManyField(GroupTag, related_name='group')

    def __str__(self):
        return self.name
