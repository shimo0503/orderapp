from rest_framework import serializers

from .models import Products, Customer, CustomerProduct, Sales


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('name', 'code', 'price', 'rest')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('made_at', 'table_number', 'paycheck', 'price', 'products')

class CustomerProductSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CustomerProduct
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ('date', 'price')