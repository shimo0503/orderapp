from django.shortcuts import render,redirect
from OrderApp.forms import AppendProductForm, RegisterRestForm
from OrderApp.models import Products
from django.core.exceptions import ObjectDoesNotExist

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


            
