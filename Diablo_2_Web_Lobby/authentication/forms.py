from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from authentication.models import PvpgnBnet
from authentication.models import CustomUser

#Form for user to register
class FormReg(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
