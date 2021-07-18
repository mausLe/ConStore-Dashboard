from django.db import models

# Create your models here.

class Watchlist(models.Model):
    studentid = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    # image = models.ImageField(upload_to='images/ ', null=True)
    image = models.TextField(null=True)

    type = models.IntegerField(null=False)

    def __str__(self):
        return self.name