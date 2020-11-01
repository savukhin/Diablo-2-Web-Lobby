from django.urls import path

from . import views

urlpatterns = [
    path('messages', views.messages, name='messages'),
    path('dialogue/subj=<int:id>', views.dialogue, name='dialogue'),
    #path('sMsg/subj=<int:dialogue_id>?author=<int:author_id>?text=<str:text>', views.sendMessage, name='sendMessage'),
    path('sMsg', views.sendMessage, name='sendMessage'),
]