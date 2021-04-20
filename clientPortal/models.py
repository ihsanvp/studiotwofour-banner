from campaign.models import Campaign
from django.db import models

# Create your models here.
class Feedback(models.Model) :
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True)
    message = models.TextField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)