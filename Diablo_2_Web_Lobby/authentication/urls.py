from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('signin', views.signIn, name='sign in'),
    path('signout', views.signOut, name='sign out'),
    path('profile/server=<str:server>;name=<str:username>', views.profile, name='profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)