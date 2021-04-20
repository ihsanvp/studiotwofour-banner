from django.shortcuts import redirect, render
from .models import Campaign
from .forms import CampaignForm, UploadBundleForm
from client.models import Client
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
import zipfile
import os 
import uuid
from bannerApp.models import Banner
from django.core.files.base import File
import shutil

# Create your views here.
@login_required()
def bundle_upload(request) :

  form = UploadBundleForm()
  context = {
    'form': form
  }

  if request.POST :
    form = UploadBundleForm(request.POST, request.FILES)

    if form.is_valid() :
      file = form.cleaned_data['file']
      client = form.cleaned_data['client']

      campaign_count = 0
      banner_count = 0

      upload_id = str(uuid.uuid4())
      banner_types = Banner.TYPES
      banner_types = list(map(lambda type : type[0], banner_types))

      temp_dir = os.path.join(default_storage.location, 'Banner', 'temp', upload_id)

      try :
        with zipfile.ZipFile(file) as zip_obj :
          zip_obj.extractall(temp_dir)

        for campaign in os.listdir(temp_dir) :
          campaign_path = os.path.join(temp_dir, campaign)
          
          campaign, created = Campaign.objects.get_or_create(name=campaign, client=client)

          if created :
            campaign_count += 1

          for banner_zip in os.listdir(campaign_path) :
            banner_type = banner_zip.replace('.zip', '')
            
            if banner_type in banner_types :

              banner_path = os.path.join(campaign_path, banner_zip)
              banner_filename = banner_zip

              banner = Banner(type=banner_type, campaign=campaign)
              f = open(banner_path, 'rb')
              banner_file = File(f)
              banner.file.save(banner_filename, banner_file, save=True)
              f.close()

              banner_count += 1

        messages.success(request, f'Added {campaign_count} Campaigns & {banner_count} Banners')
      except Exception as error :
        messages.error(request, str(error))


      shutil.rmtree(temp_dir, ignore_errors=True)        

    
    else :
      messages.error(request, 'Bundle Upload failed')

  return render(request, 'campaign/bundle_upload.html', context=context)

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