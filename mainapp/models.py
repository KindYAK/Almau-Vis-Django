from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    price = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    is_adult = models.BooleanField(default=False)

    parent_category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField()
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    datetime = models.DateTimeField()
    price = models.PositiveSmallIntegerField()
    review = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Order from {self.client} - {self.product} ({self.price}$)"
