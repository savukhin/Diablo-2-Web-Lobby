from django.db import models
from authentication.models import CustomUser
from django.core.validators import RegexValidator

# Create your models here.

#Validator for charField to not contain figures
nonFigureRegex = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')


class Character(models.Model):
    name = models.CharField(max_length=16, blank=False, null=False, unique=True, validators=[nonFigureRegex])
    player = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    characterClass = models.CharField(max_length=11, blank=False, null=False)
