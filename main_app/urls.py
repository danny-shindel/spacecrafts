from django.urls import path
from . import views
from main_app.views import Index



urlpatterns = [
  path('', Index.as_view(), name='index'),
  path('crafts/', views.user_index, name='crafts'),
  path('search/', views.search, name='search'),
  path('form/', views.form, name='form'),
]