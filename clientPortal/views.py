from django.shortcuts import render
from client.models import Client
from campaign.models import Campaign
from bannerApp.models import Banner
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404

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


def test(request) :

  TYPES = (
        ('120x240', '120x240'),
        ('120x600', '120x600'),
        ('160x600', '160x600'),
        ('200x200', '200x200'),
        ('250x250', '250x250'),
        ('300x50', '300x50'),
        ('300x250', '300x250'),
        ('300x600', '300x600'),
        ('300x1050', '300x1050'),
        ('320x50', '320x50'),
        ('320x100', '320x100'),
        ('320x240', '320x240'),
        ('320x480', '320x480'),
        ('336x280', '336x280'),
        ('468x60', '468x60'),
        ('728x90', '728x90'),
        ('970x90', '970x90'),
        ('970x250', '970x250'),
    )

  context = {
    'banner': Banner.objects.first(),
    'types': TYPES
  }

  return render(request, 'clientPortal/test.html', context=context)




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

  banners = campaign.banner.all().order_by('type')

  context = {
    'client':client,
    'campaign':campaign,
    'banners': banners,
    'count': range(9)
  }

  print(banners)

  if campaign.published :
    return render(request, 'clientPortal/client_page.html', context)
  else :
    return HttpResponseNotFound('<h1>Page not found</h1>')



def publish(request, id) :
  campaign = Campaign.objects.get(id=id)
  campaign.published = True
  campaign.save()

  return JsonResponse({'action': 'published'})


def block(request, id) :
  campaign = get_object_or_404(Campaign, pk=id)
  campaign.published = False
  campaign.save()

  return JsonResponse({'action': 'blocked'})