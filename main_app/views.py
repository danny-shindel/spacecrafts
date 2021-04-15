from django.shortcuts import render, redirect
from .models import Craft
from .forms import CraftForm
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class Index(ListView):
    model = Craft
    fields = ['name']
    
def user_index(request):
    crafts = Craft.objects.filter(user=request.user)
    return render(request, 'spacecrafts/index.html', { 'crafts': crafts })

def search(request):
    response = requests.get('https://swapi.dev/api/starships')
    results = response.json()
    starships = results['results']
    response2 = requests.get('https://swapi.dev/api/vehicles')
    results2 = response2.json()
    vehicles = results2['results']
    return render(request, 'spacecrafts/search.html', { 'starships': starships, 'vehicles' : vehicles })

def form(request):
    response = requests.get(request.POST["url"])
    results = response.json()
    print(results)
    craft_form = CraftForm(results)
    return render(request, 'spacecrafts/form.html', { 'craft_form' : craft_form , 'url' : results['url']}) #end point at url in request.post

def create(request):
    form = CraftForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.url = request.POST['url']
        instance.save()
    return redirect('crafts')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class CraftUpdate(UpdateView):
    model = Craft
    fields = ['cargo_capacity', 'consumables', 'cost_in_credits', 'crew', 'length', 
    'manufacturer', 'max_atmosphering_speed', 'model', 'name', 'passengers', 
    'hyperdrive_rating', 'vehicle_class', 'starship_class', 'MGLT', 'sell_price', 
    'condition', 'description', 'mileage'] 
# get_absolute_url ?

class CraftDelete(DeleteView):
    model = Craft
    success_url = '/crafts/'

class CraftDetail(DetailView):
    model = Craft
    fields = '__all__'

