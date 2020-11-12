from django.shortcuts import render,redirect
from .forms import UserCreationForm,UserLoginForm
from django.contrib.auth import login,logout

# Create your views here.

def signup(request,*args,**kargs):

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')

    return render(request,'signup.html',{'form':form})

def login(request,*args,**kargs):

    form = UserLoginForm(request.POST or None)
    
    if form.is_valid():
        
        
        user = form.cleaned_data.get('object')
        print(user,user.email)
        login(request,user)
        return redirect('products')

    return render(request,'login.html',{'form':form})              


def log_out(request):
    logout(request)
    return redirect('home')