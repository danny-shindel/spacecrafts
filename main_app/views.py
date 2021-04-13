from django.shortcuts import render, redirect
from .models import Craft
from .forms import CraftForm
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
    response = requests.get(request.POST["url"])
    results = response.json()
    print(results)
    craft_form = CraftForm(results)
    return render(request, 'spacecrafts/form.html', { 'craft_form' : craft_form }) #end point at url in request.post

def create(request):
    form = CraftForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    return redirect('/')

