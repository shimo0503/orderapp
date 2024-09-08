from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('front')
        else:
            error = "ユーザー名もしくはパスワードが間違っています。"
            return render(request, 'registration/login.html', {'error':error})
    else:
        return render(request, 'registration/login.html')
