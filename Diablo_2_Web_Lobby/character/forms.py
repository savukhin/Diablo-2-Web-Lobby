from django.contrib.auth.models import User
from django import forms
from character.models import Character

#Form for user to register
class CharacterCreateForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'characterClass']
