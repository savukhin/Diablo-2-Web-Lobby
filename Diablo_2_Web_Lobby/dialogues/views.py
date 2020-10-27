from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def messages(request):
    return render(request, template_name='messages.html')
