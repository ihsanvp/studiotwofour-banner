from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.
class Client(models.Model) :
  name = models.CharField(max_length=50, null=True, unique=True)
  date = models.DateField(auto_now_add=True, null=True)
  
  def __str__(self) :
    return self.name

  def readable_name(self) :
      return self.name.replace('-', ' ')
@receiver(pre_save, sender=Client)
def format_name_client(sender, instance, **kwargs) :
    instance.name = instance.name.replace(' ', '-')
