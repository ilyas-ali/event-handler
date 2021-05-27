from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.TextField(null=True)
    des = models.TextField(null=True)
    url=models.URLField(null=True)

    def __str__(self):
        return self.name

class Non_interesting(models.Model):
    url=models.URLField(null=True)
    def __str__(self):
        return self.url