from django.shortcuts import render
from .models import Craft
from django.views.generic import ListView
import requests

# Create your views here.

class Index(ListView):
    model = Craft
    fields = ['name']
    
def user_index(request):
    crafts = Craft.objects.all()
    return render(request, 'spacecrafts/index.html', { 'crafts': crafts })

def search(request):
    response = requests.get('https://swapi.dev/api/starships')
    results = response.json()
    starships = results['results']
    return render(request, 'spacecrafts/search.html', { 'starships': starships })

def form(request):
    test = request.POST
    return render(request, 'spacecrafts/form.html', { 'test': test })

