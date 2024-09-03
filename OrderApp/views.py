from django.shortcuts import render,redirect
from OrderApp.forms import AppendProductForm, RegisterRestForm, OrderForm, PayForm, ProvideForm
from OrderApp.models import Products, CustomerProduct, Customer
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
import os
import csv

#メインページを表示
def frontpage(request):
    return render(request, "frontpage.html")

#メニュー追加画面
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
def restcheck(request):
    products = Products.objects.all()
    return render(request,"restcheck.html",{"products": products})

#残数登録
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

def provided(request):
    try:
        customer_products = CustomerProduct.objects.filter(provided=True)
    except:
        return render(request, 'unprovided.html')
    return render(request, 'unprovided.html', {'customer_products': customer_products})

def unprovided(request):
    try:
        customer_products = CustomerProduct.objects.filter(provided=False).order_by('made_at')
    except:
        return render(request, 'unprovided.html')
    return render(request, 'unprovided.html', {'customer_products': customer_products})

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

def pay(request):
    customers = Customer.objects.all()
    return render(request, 'pay.html', {'customers': customers})

def payflow(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.paycheck = True
    customer.save()
    return redirect('pay')

def payreverse(request):
    customers = Customer.objects.all()
    return render(request, 'payreverse.html', {'customers': customers})

def payreverseflow(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.paycheck = False
    customer.save()
    return redirect('payreverse')

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

def csv_install(request, filename):
    file_path = os.path.join('media/sales.csv', filename)
    
    if not os.path.exists(file_path):
        return HttpResponse("File not found.", status=404)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response