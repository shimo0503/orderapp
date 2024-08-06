from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=255,blank=False)
    code = models.CharField(max_length=255,blank=False)
    price = models.IntegerField(null=False,blank=False)
    order_num = models.IntegerField(null=True,blank=True)
    rest = models.IntegerField(null=True,blank=True)

class Customer(models.Model):
    table_number = models.IntegerField(null=True,blank=True)
    paycheck = models.BooleanField(null=False,blank=False)
    price = models.IntegerField(null=True,blank=True)
    products = models.ManyToManyField(Products,null=False,blank=False)

