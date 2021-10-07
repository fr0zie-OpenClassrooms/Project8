from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    brands = models.CharField(max_length=200)
    stores = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1)
    url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
