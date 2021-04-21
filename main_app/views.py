from django.shortcuts import render, redirect
from .models import Craft, Favorite, Photo, Badge
from .forms import CraftForm
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
import requests
import uuid
import boto3
import os
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Index(ListView):
    model = Craft
    fields = ['name']

    def get_context_data(self, **kwargs):
        if (not self.request.user.is_anonymous):
            context = super().get_context_data(**kwargs)
            library = []
            favs = Favorite.objects.filter(user = self.request.user)
            for fav in favs:
                library.append(fav.__dict__['craft_id'])
            context['favs'] = library
            return context
        else:
            context = super().get_context_data(**kwargs)
            context['object_list'] = Craft.objects.all()
            return context
            
    
        

@login_required
def user_index(request):
    crafts = Craft.objects.filter(user=request.user)
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
    craft_form = CraftForm(results)
    badges = Badge.objects.all()
    return render(request, 'spacecrafts/form.html', { 'craft_form' : craft_form , 'url' : results['url'], 'badges' : badges}) #end point at url in request.post

@login_required
def create(request):
    form = CraftForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.url = request.POST['url']
        instance.save()
        for badge in request.POST.getlist('badges'):
            instance.badges.add(int(badge))
        photo_file = request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                Photo.objects.create(url=url, craft_id=instance.__dict__['id'])
            except:
                print('An error occurred uploading file to S3')
    return redirect('crafts')

@login_required
def favorite_index(request):
    favs = request.user.favorite_set.all()
    return render(request, 'spacecrafts/favorite.html', { 'favs' : favs }) 

@login_required
def favorite_create(request, craft_id):
    favs = request.user.favorite_set.all()
    for fav in favs:
        if (craft_id == fav.__dict__['craft_id']):
            fav.delete()
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

def craft_update(request, craft_id):
    craft = Craft.objects.get(id=craft_id)
    if craft.__dict__['user_id'] == request.user.id:
        photos  = Photo.objects.filter(craft = craft_id)
        print(photos)
        badges_not = Badge.objects.exclude(id__in = craft.badges.all().values_list('id'))
        form = CraftForm(craft.__dict__)
        return render(request, 'main_app/craft_form.html', {'form' : form, 'craft' : craft, 'badges' : badges_not, 'photos': photos})
    else:
        return redirect('index')


def edit(request, craft_id):
    instance = Craft.objects.get(id=craft_id)
    form = CraftForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        for badge in request.POST.getlist('badges'):
            instance.badges.add(int(badge))
        for badge in request.POST.getlist('badges_has'):
            instance.badges.remove(int(badge))
        for photo in request.POST.getlist('photos'):
            Photo.objects.get(id = photo).delete()
        photo_file = request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                Photo.objects.create(url=url, craft_id=instance.__dict__['id'])
            except:
                print('An error occurred uploading file to S3')
        return redirect('crafts')
    return redirect('crafts')

class CraftDelete(DeleteView, LoginRequiredMixin):
    model = Craft
    success_url = '/crafts/'

class CraftDetail(DetailView, LoginRequiredMixin):
    model = Craft
    fields = '__all__'

    def get_context_data(self, **kwargs):
        if (not self.request.user.is_anonymous):
            context = super().get_context_data(**kwargs)
            library = []
            favs = Favorite.objects.filter(user = self.request.user)
            for fav in favs:
                library.append(fav.__dict__['craft_id'])
            context['favs'] = library
            return context
        else:
            context = super().get_context_data(**kwargs)
            context['object_list'] = Craft.objects.all()
            return context
