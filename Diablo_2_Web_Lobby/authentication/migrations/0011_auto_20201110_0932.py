# Generated by Django 2.2.16 on 2020-11-10 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_auto_20201110_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='ssh', max_length=32, unique=True),
            preserve_default=False,
        ),
    ]
