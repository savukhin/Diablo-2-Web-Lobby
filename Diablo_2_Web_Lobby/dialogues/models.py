from django.db import models
from authentication.models import CustomUser
import datetime
# Create your models here.


class Dialogue(models.Model):
    users = models.ManyToManyField(to=CustomUser)

''' TODO: CHAT
class Chat(models.Model):
    users = models.ManyToManyField(to=CustomUser)
    title = models.CharField(max_length=128, null=False, blank=False)
    photo = models.ImageField(upload_to='ChatPhotos',
                              default='ChatPhotos/blankChatPhoto/blankChatPhoto.jpg')
'''

class Message(models.Model):
    Author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name="Автор сообщения")
    text = models.TextField(verbose_name='Содержимое сообщения')
    date = models.DateTimeField(verbose_name='Дата отправления', auto_now_add=True)
    is_read = models.BooleanField(verbose_name='Было ли прочитано сообщение', default=False)
    dialogue = models.ForeignKey(to=Dialogue, on_delete=models.CASCADE, verbose_name='Ссылка на диалог')

    class Meta:
        ordering = ['date']
