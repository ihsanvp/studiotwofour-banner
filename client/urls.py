from django.urls import path
from . import views

urlpatterns = [
  path('', views.client_home, name='client_home'),

  path('add/', views.add_client, name='add_client'),
  path('delete/<int:pk>', views.delete_client, name='delete_client'),
  path('edit/<int:pk>', views.edit_client, name='edit_client'),

  path('actions/', views.bulk_actions, name='client_bulk_actions')
  
]