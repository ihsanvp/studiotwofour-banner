from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import ClientForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required()
def client_home(request) :

  clients = Client.objects.all().order_by('id')
  paginator = Paginator(clients, 15)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'page_obj':page_obj,
  }
  return render(request, 'client/home.html', context)

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
        client = Client.objects.get(name=name)
        client.delete()

      if items_count > 0 :
        messages.success(request, 'Successfully deleted %i Client(s)'%(items_count))
      elif items_count == 0 :
        messages.error(request, 'No Clients selected')

  return redirect('client_home')


@login_required()
def add_client(request) :
  form = ClientForm()
  if request.POST :
    form = ClientForm(request.POST)
    if form.is_valid() :
      name = form.cleaned_data['name']
      form.save()

      messages.success(request, 'The Client "%s" was added successfully'%(name))

      return redirect('client_home')
  context = {
    'form':form
  }
  return render(request, 'client/add.html', context)


@login_required()
def delete_client(request, pk) :
  client = Client.objects.get(id=pk)
  client.delete()
  messages.info(request, 'The Client "%s" was deleted successfully'%(client.readable_name()))
  return redirect('client_home')


def edit_client(request, pk) :
  instance = Client.objects.get(id=pk)
  form = ClientForm(instance=instance)
  if request.POST :
    form = ClientForm(request.POST, instance=instance)
    if form.is_valid() :
      name = form.cleaned_data['name']
      form.save()

      messages.info(request, 'The Client "%s" was changed successfully'%(name))

      return redirect('client_home')

  context = {
    'form':form,
    'instance':instance,
  }
  return render(request, 'client/edit.html', context)