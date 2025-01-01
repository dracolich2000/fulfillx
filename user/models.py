from django.db import models

# Create your models here.

class Shop(models.Model):
    shop_url = models.CharField(max_length=255, unique=True)
    access_token = models.TextField()