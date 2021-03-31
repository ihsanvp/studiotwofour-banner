from django.shortcuts import redirect, render
from .models import Campaign
from .forms import CampaignForm
from client.models import Client
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required()
def campaign_home(request) :

  campaigns = Campaign.objects.all().order_by('id')
  clients = Client.objects.all()

  paginator = Paginator(campaigns, 15)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'page_obj':page_obj,
    'clients':clients,
  }
  return render(request, 'campaign/home.html', context)

@login_required()
def bulk_actions(request) :
  if request.POST :
    data = request.POST
    action = data.get('action')
    result = data.keys()
    items = [entry for entry in result]
    items = items[2:]
    items_count = len(items)

    if action == 'delete' :
      for name in items :
        campaign = Campaign.objects.get(name=name)
        campaign.delete()

      if items_count > 0 :
        messages.success(request, 'Successfully deleted %i Campaign(s)'%(items_count))
      elif items_count == 0 :
        messages.error(request, 'No Campaigns selected')

  return redirect('campaign_home')

@login_required()
def delete_campaign(request, pk) :
  campaign = Campaign.objects.get(id=pk)
  campaign.delete()
  messages.info(request, 'The Campaign "%s" was deleted successfully'%(campaign.readable_name()))
  return redirect('campaign_home')

@login_required()
def add_campaign(request) :
  form = CampaignForm()
  if request.POST :
    form = CampaignForm(request.POST)
    if form.is_valid() :
      name = form.cleaned_data['name']
      form.save()

      messages.success(request, 'The Campaign "%s" was added successfully'%(name))

      return redirect('campaign_home')

  context = {
    'form':form,
  }
  return render(request, 'campaign/add.html', context)


@login_required()
def edit_campaign(request, pk) :
  instance = Campaign.objects.get(id=pk)
  form = CampaignForm(instance=instance)
  if request.POST :
    form = CampaignForm(request.POST, instance=instance)
    if form.is_valid() :
      name = form.cleaned_data['name']
      form.save()

      messages.info(request, 'The Client "%s" was changed successfully'%(name))

      return redirect('campaign_home')

  context = {
    'form':form,
    'instance':instance,
  }
  return render(request, 'campaign/edit.html', context)