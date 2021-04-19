from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

import os
# from zipfile import ZipFile
import zipfile

from .scripts import manage_zip_upload

from campaign.models import Campaign

def upload_path_handler(instance, filename):
    name = instance.name
    return "Banner/zip/%s/%s" %(name, filename)

class Banner(models.Model) :

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

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='banner')
    name = models.CharField(max_length=50, unique=True)
    file = models.FileField(upload_to=upload_path_handler)
    type = models.CharField(max_length=20, choices=TYPES)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return  self.name + '   ' + self.type

    def readable_name(self) :
      return self.name.replace('-', ' ')
@receiver(pre_save, sender=Banner)
def format_name_banner(sender, instance, **kwargs) :
    instance.name = instance.name.replace(' ', '-')


@receiver(post_save, sender=Banner)
def extract_banner(sender, instance, **kwargs):
    file = instance.file.path

    tempDir = os.path.join(settings.BASE_DIR, 'media', 'Banner', 'temp', instance.name)
    targetDir = os.path.join(settings.BASE_DIR, 'assets', 'banner')

    # Make  temp Directory
    if not os.path.exists(tempDir) :
        os.makedirs(tempDir)

    # Make  target Directory
    if not os.path.exists(targetDir) :
        os.makedirs(targetDir)

    # Extract Eng to temp
    with zipfile.ZipFile(file) as zipObj :
        zipObj.extractall(tempDir)

    # Manage Eng Zip
    manage_zip_upload(instance, tempDir, targetDir)





