from django.shortcuts import render,redirect
from OrderApp.forms import AppendProductForm, RegisterRestForm, OrderForm, PayForm, ProvideForm
from OrderApp.models import Products, CustomerProduct, Customer, Sales
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import csv
from .serializer import ProductSerializer, CustomerSerializer, SaleSerializer
from rest_framework import viewsets

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


#メインページを表示
@login_required
def frontpage(request):
    return render(request, "frontpage.html")

# 全商品取得 /api/product
# postでprovided: trueなら提供済みを、falseなら未提供を返す
@method_decorator(csrf_exempt, name='dispatch')
class ProductAPIView(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'status' : '200',
            'data' : serializer.data
        }, status = 200)
    def post(self, request):
        if request.data.get('provided'):
            customer_products = CustomerProduct.objects.filter(provided=True)
            return Response({
                'status' : '200',
                'data' : customer_products.values()
            }, status = 200)
        else:
            customer_products = CustomerProduct.objects.filter(provided=False)
            return Response({
                'status' : '200',
                'data' : customer_products.values()
            }, status = 200)

class CustomerAPIView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({
            'status' : '200',
            'data' : serializer.data
        }, status = 200)

# 新メニュー追加 /api/newMenu
class NewMenu(APIView):
    def post(self, request):
        name = request.data.get('name')
        price = request.data.get('price')
        # すでにある名前で登録しようとしたら失敗させる
        if Products.objects.filter(name=name).exists():
            return Response({
                "status" : '400',
                "data" : 'その名前は既に存在しています。'
            }, status = 400)
        elif not price:
            return Response({
                "status" : '400',
                "data" : '値段が設定されていません。'
            }, status = 400)
        else:
            Products.objects.create(
                name=name,
                code="",
                price=price,
                rest=0
            )
            return Response({
                "status" : '201',
                "data" : 'success'
            }, status = 201)
        
# メニューの削除
class DeleteMenu(APIView):
    def post(self, request):
        try:
            product = Products.objects.get(name=request.data.get('name'))
            product.delete()
            return Response({
                "status" : '201',
                "data" : 'success'
            }, status = 201)
        except:
            return Response({
                "status" : '400',
                "data" : "Request Error."
            }, status = 400)

# 残数登録 /api/rest
class RestRegister(APIView):
    def post(self, request):
        name = request.data.get('name')
        if name:
            try:
                product = Products.objects.get(name=name)
                serializer = ProductSerializer(product)
                product.rest = request.data.get('rest')
                product.save()
                return Response({
                    "status" : '201',
                    "data" : "success"
                }, status = 201)
            except:
                return Response({
                    "status" : '400',
                    "data" : "Cannot find data."
                }, status = 400)
        else:
            return Response({
                "status" : '400',
                "data" : "Request Error. No name field."
            }, status = 400)

# 新規注文 /api/order/new
'''
request body
{
    "table": num,
    "data": 
    [
        "name" : string,
        "quantity": num
    ]
}
'''
class NewOrder(APIView):
    def post(self, request):
        table = request.data.get('table_number')
        if table and Customer.objects.filter(table_number=table).exists():
            return Response({
                "status" : '400',
                "data" : "その卓は既に使用済みです。"
            }, status = 400)
        elif not table:
            return Response({
                "status" : '400',
                "data" : "Request Error. No table_number field."
            }, status = 400)
        else:
            customer = Customer.objects.create(
                table_number=table,
            )
            products = Products.objects.all()
            for data in request.data.get('data'):
                for product in products:
                    if product.name == data['name']:
                        quantity = data['quantity']
                        if product.rest - quantity >= 0:
                            customer.price += product.price * quantity
                            product.rest -= quantity
                            product.save()
                            customer.save()
                            CustomerProduct.objects.create(
                                customer=customer,
                                product=product,
                                quantity=quantity
                            )
                        else:
                            customer.delete()
                            return Response({
                                "status" : '400',
                                "data" : "残数が足りないので送信できません。"
                            }, status = 400)
            return Response({
                "status" : '201',
                "data" : "success"
            }, status = 201)

# 追加注文(残数足りない時にバグりそう)
class AddOrder(APIView):
    def post(self, request):
        table = request.data.get('table_number')
        if table and not Customer.objects.filter(table_number=table).exists():
            return Response({
                "status" : '400',
                "data" : "その卓は使用されていません。"
            }, status = 400)
        elif not table:
            return Response({
                "status" : '400',
                "data" : "Request Error. No table_number field."
            }, status = 400)
        else:
            customer = Customer.objects.get(
                table_number=table,
            )
            products = Products.objects.all()
            for data in request.data.get('data'):
                for product in products:
                    if product.name == data['name']:
                        quantity = data['quantity']
                        if product.rest - quantity >= 0:
                            customer.price += product.price * quantity
                            product.rest -= quantity
                            product.save()
                            customer.save()
                            CustomerProduct.objects.create(
                                customer=customer,
                                product=product,
                                quantity=quantity
                            )
                        else:
                            return Response({
                                "status" : '400',
                                "data" : "残数が足りないので送信できません。"
                            }, status = 400)
            return Response({
                "status" : '201',
                "data" : "success"
            }, status = 201)

# 提供済みか済みじゃない商品を表示
class Provide(APIView):
    def post(self, request):
        try:
            customer_product = CustomerProduct.objects.get(name = request.data.get('name'))
            if customer_product.provided:
                customer_product.provided = False
                customer_product.save()
                return Response({
                    "status" : '201',
                    "data" : "success"
                }, status = 201)
            else:
                customer_product.provided = True
                customer_product.save()
                return Response({
                    "status" : '201',
                    "data" : "success"
                }, status = 201)
        except:
            return Response({
                "status" : '400',
                "data" : "Request Error."
            }, status = 400)

# 支払い
class Pay(APIView):
    def post(self, request):
        table = request.data.get('table_number')
        if table and Customer.objects.filter(table_number=table).exists():
            customer = Customer.objects.get(table_number = table)
            Sales.objects.create(
                price=customer.price
            )
            customer.delete()
            return Response({
                "status" : '201',
                "data" : "success"
            }, status = 201)
        else:
            return Response({
                "status" : '400',
                "data" : "Request Error."
            }, status = 400)

# 売上表示
class displaySales(APIView):
    def get(self, request):
        sales = Sales.objects.get()
        serializer = SaleSerializer(Sales, mamy=True)
        return Response({
            "status" : '200',
            "data" : sales.values()
        }, status = 201)          
@login_required
def minus_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            table_number = form.cleaned_data['customer_table_number']
            
            # または、すでにテーブル番号が存在するかどうかをチェックして、既存の顧客を取得
            customer, created = Customer.objects.get_or_create(
                table_number=table_number,
                defaults={'paycheck': False, 'price': 0}
            )
            #追加注文で未注文卓にアクセスした場合
            if created == True:
                customer.delete()
                form = OrderForm()
                error = "未使用卓です。"
                return render(request,"neworder.html", {'error': error, 'form': form})
            else:
                products = Products.objects.all()
                for product in products:
                    quantity = form.cleaned_data.get(f'quantity_{product.id}', 0)
                    if quantity > 0:
                        CustomerProduct.objects.create(
                            customer=customer,
                            product=product,
                            quantity=-quantity
                        )
                        customer.price -= product.price * quantity
                        product.rest += quantity
                        product.save()
                        customer.save()
                        
                return render(request, 'order_success.html')  # 成功した後のリダイレクト先
    else:
        form = OrderForm()
        
    return render(request, 'neworder.html', {'form': form})