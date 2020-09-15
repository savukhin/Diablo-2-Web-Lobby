from django.urls import path

from . import views

urlpatterns = [
    path('signin', views.signIn, name='sign in'),
    path('signup', views.signUp, name='sign up'),
    path('signout', views.signOut, name='sign out'),
]