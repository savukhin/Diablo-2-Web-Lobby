from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.index, name='sign in'),
    path('signout', views.index, name='sign out'),
    path('signup', views.index, name='sign up'),
]