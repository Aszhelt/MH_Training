from django.db import models


class GroupTag(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='storage/groups/')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    group = models.ManyToManyField(GroupTag, related_name='tags')

    def __str__(self):
        return self.name


class Item(models.Model):

    name = models.CharField(max_length=300, unique=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='storage/items/')
    tags = models.ManyToManyField(Tag, related_name='tags')

    def __str__(self):
        return self.name
