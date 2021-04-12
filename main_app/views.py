from django.shortcuts import render
from .models import Craft
from django.views.generic import ListView

# Create your views here.

class Index(ListView):
    model = Craft
    fields = ['name']
    

