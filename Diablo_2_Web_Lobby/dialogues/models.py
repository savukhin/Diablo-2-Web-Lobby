from django.db import models
from authentication.models import CustomUser
import datetime
# Create your models here.


class Dialogue(models.Model):
    users = models.ManyToManyField(to=CustomUser)


class Message(models.Model):
    Author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name="Автор сообщения")
    text = models.TextField(verbose_name='Содержимое сообщения')
    date = models.DateField(verbose_name='Дата отправления', default=datetime.date.today)
    is_read = models.BooleanField(verbose_name='Было ли прочитано сообщение', default=False)
    dialogue = models.ForeignKey(to=Dialogue, on_delete=models.CASCADE, verbose_name='Ссылка на диалог')

    class Meta:
        ordering = ['date']
