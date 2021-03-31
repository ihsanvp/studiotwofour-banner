from django.urls import path
from . import views

urlpatterns = [
  path('', views.banner_home, name='banner_home'),

  path('add/', views.add_banner, name='add_banner'),
  path('delete/<int:pk>', views.delete_banner, name='delete_banner'),
  path('edit/<int:pk>', views.edit_banner, name='edit_banner'),

  path('actions/', views.bulk_actions, name='banner_bulk_actions'),
]