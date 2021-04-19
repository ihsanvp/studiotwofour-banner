from django.urls import path
from . import views

urlpatterns = [
  path('campaign/clientPortal', views.home, name='client_portal_home'),
  path('<str:client_name>/<str:campaign_name>/', views.client_page, name='client_page'),

  path('test/', views.test)

]