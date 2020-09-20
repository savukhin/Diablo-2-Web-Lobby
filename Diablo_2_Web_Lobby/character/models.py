from django.db import models
from authentication.models import CustomUser

# Create your models here.


class Character(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    player = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    characterClass = models.CharField(max_length=11, blank=False, null=False)
