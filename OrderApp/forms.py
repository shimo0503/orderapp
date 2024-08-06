from django import forms
from OrderApp.models import Products
from OrderApp.models import Customer

class AppendProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["name","code","price"]
        labels = {"name":" 商品名",
                  "code": "商品コード",
                  "price": "価格"}

class RegisterRestForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["name","rest"]
        labels = {"name": "名前", "rest": "残数"}

class OrderForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["table_number","products"]
        labels = {"table_number": "卓番",
                  "products": "商品"}
