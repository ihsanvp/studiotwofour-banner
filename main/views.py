from django.shortcuts import redirect, render
from django.contrib.auth import login as my_login, authenticate
from django.contrib.auth .decorators import login_required
from client.models import Client
from campaign.models import Campaign
from bannerApp.models import Banner

# Create your views here.
@login_required()
def home(request) :

  clients = Client.objects.all()
  campaigns = Campaign.objects.all()
  banners = Banner.objects.all()

  context = {
    'clients':clients,
    'campaigns':campaigns,
    'banners':banners,
  }
  return render(request, 'main/home.html', context)

