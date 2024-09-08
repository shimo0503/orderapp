from django import forms
from OrderApp.models import Customer, Products, CustomerProduct

class AppendProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["name","price"]
        labels = {"name":" 商品名",
                  "price": "価格"}

class RegisterRestForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["name","rest"]
        labels = {"name": "名前", "rest": "残数"}

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['table_number']
        labels = {
            'table_number': 'テーブル番号',
        }
        widgets = {
            'table_number': forms.NumberInput(attrs={'placeholder': 'テーブル番号'}),
        }

class CustomerProductForm(forms.ModelForm):
    class Meta:
        model = CustomerProduct
        fields = ['customer', 'product', 'quantity']
        labels = {
            'customer': '顧客',
            'product': '商品',
            'quantity': '数量',
        }
        widgets = {
            'customer': forms.Select(),
            'product': forms.Select(),
            'quantity': forms.NumberInput(attrs={'min': 0}),
        }

class OrderForm(forms.Form):
    customer_table_number = forms.IntegerField(
        label='テーブル番号',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'テーブル番号'})
    )
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        products = Products.objects.all()
        for product in products:
            self.fields[f'quantity_{product.id}'] = forms.IntegerField(
                label=product.name,
                initial=0,
                min_value=0,
                required=False,
                widget=forms.NumberInput(attrs={'placeholder': '数量'})
            )

class PayForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['paycheck']
        labels = {'paycheck':'会計'}
        widgets = {
            'paycheck': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProvideForm(forms.ModelForm):
    class Meta:
        model = CustomerProduct
        fields = ['provided']
        labels = {'provided':'提供'}
