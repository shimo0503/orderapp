from django.contrib import admin
from .models import Products, Customer, CustomerProduct

@admin.register(Products)
@admin.register(Customer)
@admin.register(CustomerProduct)
class ProductsAdmin(admin.ModelAdmin):
    pass