from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

import os
# from zipfile import ZipFile
import zipfile

from .scripts import manage_zip_upload

from campaign.models import Campaign

# Create your models here.

# def upload_path_handler(instance, filename):
#     name = instance.name
#     return "Banner/%s/%s" %(name, filename)

def upload_path_handler(instance, filename):
    name = instance.name
    return "Banner/zip/%s/%s" %(name, filename)

class Banner(models.Model) :

    TYPE = (
        ('120x600', '120x600'),
        ('160x600', '160x600'),
        ('250x250', '250x250'),
        ('300x250', '300x250'),
        ('300x600', '300x600'),
        ('320x50', '320x50'),
        ('320x100', '320x100'),
        ('336x280', '336x280'),
        ('728x90', '728x90'),
        ('970x90', '970x90'),
    )

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='banner')
    name = models.CharField(max_length=50, unique=True)
    file_eng = models.FileField(upload_to=upload_path_handler, null=True)
    file_ar = models.FileField(upload_to=upload_path_handler, null=True)
    type = models.CharField(max_length=20, choices=TYPE)
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
    print('started extract')
    file_eng = instance.file_eng.path
    file_ar = instance.file_ar.path

    tempDir_eng = os.path.join(settings.BASE_DIR, 'media', 'Banner', 'temp', 'eng', instance.name)
    tempDir_ar = os.path.join(settings.BASE_DIR, 'media', 'Banner', 'temp', 'ar', instance.name)

    targetDir_eng = os.path.join(settings.BASE_DIR, 'assets', 'banner', 'eng')
    targetDir_ar = os.path.join(settings.BASE_DIR, 'assets', 'banner', 'ar')

    # Make Eng temp Directory
    if not os.path.exists(tempDir_eng) :
        os.makedirs(tempDir_eng)

    # Make Ar temp Directory
    if not os.path.exists(tempDir_ar) :
        os.makedirs(tempDir_ar)

    # Make Eng target Directory
    if not os.path.exists(targetDir_eng) :
        os.makedirs(targetDir_eng)

    # Make Ar target Directory
    if not os.path.exists(targetDir_ar) :
        os.makedirs(targetDir_ar)

    # Extract Eng to temp
    with zipfile.ZipFile(file_eng) as zipObj_eng :
        zipObj_eng.extractall(tempDir_eng)

    # Extract Ar to temp
    with zipfile.ZipFile(file_ar) as zipObj_ar :
        zipObj_ar.extractall(tempDir_ar)

    # Manage Eng Zip
    manage_zip_upload(instance, tempDir_eng, targetDir_eng)

    # Manage Ar Zip
    manage_zip_upload(instance, tempDir_ar, targetDir_ar)



# @receiver(post_delete, sender=Banner)
# def submission_delete(sender, instance, **kwargs):
#     instance.file_eng.delete(False)
#     instance.file_ar.delete(False)

#     file = instance.name
#     directory_eng = os.path.join(settings.BASE_DIR, 'assets', 'banner', 'eng', file)
#     directory_ar = os.path.join(settings.BASE_DIR, 'assets', 'banner', 'ar', file)

#     shutil.rmtree(directory_eng, ignore_errors=True)
#     shutil.rmtree(directory_ar, ignore_errors=True)

#     directory = os.path.join(settings.BASE_DIR, 'media', 'Banner', file)

#     shutil.rmtree(directory, ignore_errors=True)

# @receiver(post_save, sender=Banner)
# def extract_banner(sender, instance, **kwargs):
#     file_eng = instance.file_eng.path
#     file_ar = instance.file_ar.path

#     directory = os.path.join(settings.BASE_DIR, 'assets')

#     if not os.path.exists(directory) :
#         os.mkdir(directory)

#     directory = os.path.join(directory, 'banner')

#     if not os.path.exists(directory) :
#         os.mkdir(directory)

#     directory_eng = os.path.join(directory, 'eng')
#     if not os.path.exists(directory_eng) :
#         os.mkdir(directory_eng)

#     directory_ar = os.path.join(directory, 'ar')
#     if not os.path.exists(directory_ar) :
#         os.mkdir(directory_ar)

#     directory_eng = os.path.join(directory_eng, instance.name)
#     if not os.path.exists(directory) :
#         os.mkdir(directory_eng)

#     directory_ar = os.path.join(directory_ar, instance.name)
#     if not os.path.exists(directory) :
#         os.mkdir(directory_eng)


#     try :
#         with ZipFile(file_eng, 'r') as zipObj :
#             val_eng = zipObj.namelist()

#             for item_eng in val_eng :
#                 if '/' in item_eng :
#                     part_eng = item_eng.split('/')

#                     print(part_eng[0])

#                     if part_eng[0] == 'images' :
#                         with ZipFile(file_eng, 'r') as zipObj :
#                             zipObj.extractall(directory_eng)
#                             print('normal')
#                             break
#                     else :
#                         print('rare')
#                         with ZipFile(file_eng, 'r') as zipObj :
#                             zipObj.extractall(os.path.join(os.path.dirname(directory_eng), 'temp'))



#                         start_eng = os.path.join(os.path.dirname(directory_eng), 'temp', part_eng[0])
#                         shutil.move(start_eng, directory_eng)
#                         shutil.rmtree(os.path.dirname(start_eng))


#                         for item in os.listdir(directory_eng) :

#                             if '.html' in item :
#                                 rename_eng = os.path.join(directory_eng, item)
#                                 os.rename(rename_eng, os.path.join(directory_eng, 'index.html'))
#                                 print('success')


#                         break
#     except :
#         pass




#     try :
#         with ZipFile(file_ar, 'r') as zipObj :
#             val_ar = zipObj.namelist()

#             for item_ar in val_ar :
#                 if '/' in item_ar :
#                     part_ar = item_ar.split('/')

#                     print(part_ar[0])

#                     if part_ar[0] == 'images' :
#                         with ZipFile(file_ar, 'r') as zipObj :
#                             zipObj.extractall(directory_ar)
#                             print('normal')
#                             break
#                     else :
#                         print('rare')
#                         with ZipFile(file_ar, 'r') as zipObj :
#                             zipObj.extractall(os.path.join(os.path.dirname(directory_ar), 'temp'))



#                         start_ar = os.path.join(os.path.dirname(directory_ar), 'temp', part_ar[0])
#                         shutil.move(start_ar, directory_ar)
#                         shutil.rmtree(os.path.dirname(start_ar))


#                         for item in os.listdir(directory_ar) :

#                             if '.html' in item :
#                                 rename_ar = os.path.join(directory_ar, item)
#                                 os.rename(rename_ar, os.path.join(directory_ar, 'index.html'))
#                                 print('success')


#                         break
#     except :
#         pass



