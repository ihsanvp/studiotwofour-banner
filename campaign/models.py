from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

from client.models import Client

# Create your models here.
class Campaign(models.Model) :
  client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='campaign')
  name = models.CharField(max_length=100)
  published = models.BooleanField(default=False)
  date = models.DateField(auto_now_add=True, null=True)

  class Meta :
      unique_together = ('client', 'name')

  def __str__(self) :
      return self.name

  def readable_name(self) :
      return self.name.replace('-', ' ')

    

    
