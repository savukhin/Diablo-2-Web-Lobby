from django.urls import path

from . import views

urlpatterns = [
    path('messages', views.messages, name='messages'),
    path('dialogue/subj=<int:id>', views.dialogue, name='dialogue'),
]