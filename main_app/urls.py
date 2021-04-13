from django.urls import path
from . import views
from main_app.views import Index



urlpatterns = [
  path('', Index.as_view(), name='index'),
  path('crafts/', views.user_index, name='crafts'),
  path('search/', views.search, name='search'),
  path('form/', views.form, name='form'),
  path('create/', views.create, name='create'),
  path('crafts/<int:pk>/update', views.CraftUpdate.as_view(), name='crafts_update'),
  path('crafts/<int:pk>/delete', views.CraftDelete.as_view(), name='crafts_delete'),
]