from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=300)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='storage/items/', blank=True)

    def __str__(self):
        return self.name
