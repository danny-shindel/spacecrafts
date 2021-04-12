from django.shortcuts import render
from .models import Craft

# Create your views here.

def home(request):
    crafts = Craft.objects.all()
    return render(request, 'home.html', {'crafts' : crafts})
