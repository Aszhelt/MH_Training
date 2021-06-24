from django.http import response
from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterForm

def home(response):
    return render(response, "core/home.html", {})

def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect('/')
    else:
        form = RegisterForm()
    return render(response, 'register/register.html', {'form':form})