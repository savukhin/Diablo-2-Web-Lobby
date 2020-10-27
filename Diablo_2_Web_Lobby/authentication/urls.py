from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('signin', views.signIn, name='sign in'),
    path('signup', views.signUp, name='sign up'),
    path('signout', views.signOut, name='sign out'),
    path('profile/<int:id>', views.profile, name='profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)