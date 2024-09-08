from django.shortcuts import render,redirect
from OrderApp.forms import AppendProductForm, RegisterRestForm, OrderForm, PayForm, ProvideForm
from OrderApp.models import Products, CustomerProduct, Customer
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import csv

#メインページを表示
@login_required
def frontpage(request):
    return render(request, "frontpage.html")

#メニュー追加画面
@login_required
def append_menu(request):
    #フォームの表示
    if request.method == "GET":
        form = AppendProductForm()
        return render(request,"append_menu.html", {"form": form})
    #送られたフォームをDBに保存する
    elif request.method == "POST":
        form = AppendProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('front')
        #バリデーションできなかったとき再びメニュー追加画面
        else:
            return render(request,"append_menu.html", {"form": form})

#残数確認
@login_required
def restcheck(request):
    products = Products.objects.all()
    return render(request,"restcheck.html",{"products": products})

#残数登録
@login_required
def restregister(request):
    if request.method == "GET":
        form = RegisterRestForm()
        return render(request,"restregister.html", {"form": form})
    elif request.method == "POST":
        form = RegisterRestForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['name']
            rest_quantities = form.cleaned_data['rest']
            try:
                product = Products.objects.get(name=product_name)
                product.rest = rest_quantities
                product.save()
                return redirect('front')
            except:
                return render(request,"restregister.html",{"form": form, "error": "その名前の商品は見つかりません"})
        else:
            return render(request,"restregister.html", {"form": form})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            table_number = form.cleaned_data['customer_table_number']
            
            # または、すでにテーブル番号が存在するかどうかをチェックして、既存の顧客を取得
            customer, created = Customer.objects.get_or_create(
                table_number=table_number,
                defaults={'paycheck': False, 'price': 0}
            )
            #新規注文で既存の顧客にアクセスした場合
            if created == False:
                form = OrderForm()
                error = "既に使われている卓です。"
                return render(request,"neworder.html", {'error': error, 'form': form})
            else:
                products = Products.objects.all()
                for product in products:
                    quantity = form.cleaned_data.get(f'quantity_{product.id}', 0)
                    if quantity > 0:
                        CustomerProduct.objects.create(
                            customer=customer,
                            product=product,
                            quantity=quantity
                        )
                        if product.rest - quantity >= 0:
                            customer.price += product.price * quantity
                            product.rest -= quantity
                            product.save()
                            customer.save()
                        else:
                            customer.delete()
                            error = "残数が足りないので送信できません"
                            form = OrderForm()
                            return render(request, 'neworder.html', {'error': error, 'form': form}) 
                return render(request, 'order_success.html')  # 成功した後のリダイレクト先
    else:
        form = OrderForm()
        
    return render(request, 'neworder.html', {'form': form})

@login_required
def addorder(request):
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
                        customer_product = CustomerProduct.objects.create(
                            customer=customer,
                            product=product,
                            quantity=quantity
                        )
                        if product.rest - quantity >= 0:
                            customer.price += product.price * quantity
                            product.rest -= quantity
                            product.save()
                            customer.save()
                        else:
                            customer_product.delete()
                            error = "残数が足りないので送信できません"
                            form = OrderForm()
                            return render(request, 'neworder.html', {'error': error, 'form': form}) 
                        
                return render(request, 'order_success.html')  # 成功した後のリダイレクト先
    else:
        form = OrderForm()
        
    return render(request, 'neworder.html', {'form': form})

@login_required
def provided(request):
    try:
        customer_products = CustomerProduct.objects.filter(provided=True)
    except:
        return render(request, 'unprovided.html')
    return render(request, 'unprovided.html', {'customer_products': customer_products})

@login_required
def unprovided(request):
    try:
        customer_products = CustomerProduct.objects.filter(provided=False).order_by('made_at')
    except:
        return render(request, 'unprovided.html')
    return render(request, 'unprovided.html', {'customer_products': customer_products})

@login_required
def provideflow(request, pk):
    customer_product = CustomerProduct.objects.get(pk=pk)
    if customer_product.provided:
        customer_product.provided = False
        customer_product.save()
        return redirect('provided')
    else:
        customer_product.provided = True
        customer_product.save()
        return redirect('unprovided')

@login_required
def pay(request):
    customers = Customer.objects.all()
    return render(request, 'pay.html', {'customers': customers})

@login_required
def payflow(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.paycheck = True
    customer.save()
    return redirect('pay')

@login_required
def payreverse(request):
    customers = Customer.objects.all()
    return render(request, 'payreverse.html', {'customers': customers})

@login_required
def payreverseflow(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.paycheck = False
    customer.save()
    return redirect('payreverse')

@login_required
def restore_csv(request):
    customers = Customer.objects.all()
    file = open('OrderApp/media/sales.csv','a',newline='')
    writer = csv.writer(file)
    for customer in customers:
        if customer.paycheck == True:
            data = [customer.made_at,customer.price]
            writer.writerow(data)
            customer.delete()
    file.close()
    return redirect('front')

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

@login_required
def menu_delete(request, pk):
    product = Products.objects.get(pk=pk)
    product.delete()
    return redirect('restcheck')

@login_required
def sales(request):
    with open('OrderApp/media/sales.csv', mode='r', encoding='utf-8') as file:
        sales = csv.reader(file)
        return render(request, 'sales.html', {'sales': sales})
    