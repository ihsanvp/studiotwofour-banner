from django.shortcuts import render
from client.models import Client
from campaign.models import Campaign
from bannerApp.models import Banner
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 

# Create your views here.
@login_required()
def home(request) :
  campaigns = Campaign.objects.all()
  paginator = Paginator(campaigns, 15)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'page_obj':page_obj
  }
  return render(request, 'clientPortal/home.html', context)




def client_page(request, client_name, campaign_name) :
  campaign = Campaign.objects.get(name=campaign_name)
  client = Client.objects.get(name=client_name)

  if request.method == 'POST' :
    data = request.POST.dict()

    msg = data.get('message')

    subject = 'Feedback from %s' %(client.readable_name())
    message = 'You have recieved a feedback from %s regarding %s.\n \nClient : %s\nCampaign : %s\n \nMESSAGE :\n%s' %(client.readable_name(), campaign.readable_name(), client.readable_name(), campaign.readable_name(), msg)

    try :
      
      
      send_mail(
              subject,
              message,
              settings.EMAIL_HOST_USER,
              ['info@studiotwofour.com'],
              fail_silently=False,
      )      

      #feedback = Feedback(campaign=campaign, message=msg, sent=True)
      #feedback.save()
    
    except :
      pass
      #feedback = Feedback(campaign=campaign, message=msg, sent=False)
      #feedback.save()

  context = {
    'client':client,
    'campaign':campaign,
  }
  return render(request, 'clientPortal/client_page.html', context)
