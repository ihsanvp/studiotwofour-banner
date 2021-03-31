from django.urls import path
from . import views

urlpatterns = [
  path('', views.campaign_home, name='campaign_home'),

  path('add/', views.add_campaign, name='add_campaign'),
  path('delete/<int:pk>', views.delete_campaign, name='delete_campaign'),
  path('edit/<int:pk>', views.edit_campaign, name='edit_campaign'),

  path('actions/', views.bulk_actions, name='campaign_bulk_actions')
]