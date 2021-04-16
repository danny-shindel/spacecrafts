from django.shortcuts import render, redirect
from .models import Craft, Favorite
from .forms import CraftForm
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Index(ListView):
    model = Craft
    fields = ['name']

@login_required
def user_index(request):
    crafts = Craft.objects.filter(user=request.user)
    print(crafts)
    return render(request, 'spacecrafts/index.html', { 'crafts': crafts })

@login_required
def search(request):
    response = requests.get('https://swapi.dev/api/starships')
    results = response.json()
    starships = results['results']
    response2 = requests.get('https://swapi.dev/api/vehicles')
    results2 = response2.json()
    vehicles = results2['results']
    return render(request, 'spacecrafts/search.html', { 'starships': starships, 'vehicles' : vehicles })

@login_required
def form(request):
    response = requests.get(request.POST["url"])
    results = response.json()
    print(results)
    craft_form = CraftForm(results)
    return render(request, 'spacecrafts/form.html', { 'craft_form' : craft_form , 'url' : results['url']}) #end point at url in request.post

@login_required
def create(request):
    form = CraftForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.url = request.POST['url']
        instance.save()
    return redirect('crafts')

def favorite_index(request):
    favs = request.user.favorite_set.all()
    return render(request, 'spacecrafts/favorite.html', { 'favs' : favs }) 


def favorite_create(request, craft_id):
    favs = request.user.favorite_set.all()
    for fav in favs:
        if (craft_id == fav.__dict__['craft_id']):
            print('same')
            return redirect('index')
    else:
        instance = Favorite()
        instance.craft_id = craft_id
        instance.user = request.user
        instance.save()
        return redirect('crafts')


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class CraftUpdate(UpdateView, LoginRequiredMixin):
    model = Craft
    fields = ['cargo_capacity', 'consumables', 'cost_in_credits', 'crew', 'length', 
    'manufacturer', 'max_atmosphering_speed', 'model', 'name', 'passengers', 
    'hyperdrive_rating', 'vehicle_class', 'starship_class', 'MGLT', 'sell_price', 
    'condition', 'description', 'mileage'] 
# get_absolute_url ?

class CraftDelete(DeleteView, LoginRequiredMixin):
    model = Craft
    success_url = '/crafts/'

class CraftDetail(DetailView, LoginRequiredMixin):
    model = Craft
    fields = '__all__'
