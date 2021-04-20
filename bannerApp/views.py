from campaign.models import Campaign
from django.shortcuts import redirect, render
from .models import Banner
from .forms import BannerForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def banner_home(request) :
  banners = Banner.objects.all().order_by('date')
  campaigns = Campaign.objects.all()

  campaign_id = request.GET.get('campaign', None)

  if  campaign_id :
    banners = Banner.objects.all().filter(campaign__id=campaign_id).order_by('type')

  paginator = Paginator(banners, 15)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'page_obj':page_obj,
    'campaigns': campaigns
  }
  return render(request, 'bannerApp/home.html', context)


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
      for id in items :
        banner = Banner.objects.get(id=id)
        banner.delete()

      if items_count > 0 :
        messages.success(request, 'Successfully deleted %i Banner(s)'%(items_count))
      elif items_count == 0 :
        messages.error(request, 'No Banner selected')
  return redirect('banner_home')


@login_required()
def delete_banner(request, pk) :
  banner = Banner.objects.get(id=pk)
  banner.delete()
  messages.info(request, 'The Banner "%s" was deleted successfully'%(banner.readable_name()))
  return redirect('banner_home')


@login_required()
def add_banner(request) :
  form = BannerForm()
  if request.POST :
    form = BannerForm(request.POST, request.FILES)
    if form.is_valid() :
      name = form.cleaned_data['name']
      form.save()

      messages.success(request, 'The Banner "%s" was added successfully'%(name))

      return redirect('banner_home')

  context = {
    'form':form,
  }
  return render(request, 'bannerApp/add.html', context)



def edit_banner(request, pk) :
  instance = Banner.objects.get(id=pk)
  form = BannerForm(instance=instance)
  if request.POST :
    form = BannerForm(request.POST, request.FILES, instance=instance)
    if form.is_valid() :
      name = form.cleaned_data['name']
      form.save()

      messages.info(request, 'The Banner "%s" was changed successfully'%(name))

      return redirect('banner_home')

  context = {
    'form':form,
    'instance':instance,
  }
  return render(request, 'bannerApp/edit.html', context)