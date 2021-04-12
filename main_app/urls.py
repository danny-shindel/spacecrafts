from django.urls import path
from . import views
from main_app.views import Index



urlpatterns = [
  path('', Index.as_view(), name='index'),
  
]

