from django.http import response
from django.shortcuts import render
from django.views import generic

def home(response):
    return render(response, "core/home.html", {})