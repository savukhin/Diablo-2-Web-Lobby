# Generated by Django 2.2.16 on 2020-11-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_customuser_server'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='pvpgn_user',
        ),
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]