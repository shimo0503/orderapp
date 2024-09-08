from django.db import models
from django.utils import timezone

class Products(models.Model):
    name = models.CharField(max_length=255,blank=False)
    code = models.CharField(max_length=255,blank=False)
    price = models.IntegerField(null=False,blank=False)
    rest = models.IntegerField(null=True,blank=True,default=0)

class Customer(models.Model):
    made_at = models.DateTimeField(auto_now=True)
    table_number = models.IntegerField(null=False,blank=False)
    paycheck = models.BooleanField(default=False)
    price = models.IntegerField(null=True,default=0)
    products = models.ManyToManyField(Products,related_name='customers')

class CustomerProduct(models.Model):
    made_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    provided = models.BooleanField(default=False)
