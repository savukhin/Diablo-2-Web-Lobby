# Generated by Django 2.2.16 on 2020-09-19 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PvpgnBnet',
            fields=[
                ('uid', models.IntegerField(primary_key=True, serialize=False)),
                ('acct_username', models.CharField(blank=True, max_length=32, null=True)),
                ('username', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('acct_userid', models.IntegerField(blank=True, null=True)),
                ('acct_passhash1', models.CharField(blank=True, max_length=40, null=True)),
                ('acct_email', models.CharField(blank=True, max_length=128, null=True)),
                ('auth_admin', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_normallogin', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_changepass', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_changeprofile', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_botlogin', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_operator', models.CharField(blank=True, max_length=6, null=True)),
                ('new_at_team_flag', models.IntegerField(blank=True, null=True)),
                ('auth_lock', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_locktime', models.IntegerField(blank=True, null=True)),
                ('auth_lockreason', models.CharField(blank=True, max_length=128, null=True)),
                ('auth_mute', models.CharField(blank=True, max_length=6, null=True)),
                ('auth_mutetime', models.IntegerField(blank=True, null=True)),
                ('auth_mutereason', models.CharField(blank=True, max_length=128, null=True)),
                ('auth_command_groups', models.CharField(blank=True, max_length=16, null=True)),
                ('acct_lastlogin_time', models.IntegerField(blank=True, null=True)),
                ('acct_lastlogin_owner', models.CharField(blank=True, max_length=128, null=True)),
                ('acct_lastlogin_clienttag', models.CharField(blank=True, max_length=4, null=True)),
                ('acct_lastlogin_ip', models.CharField(blank=True, max_length=16, null=True)),
                ('acct_ctime', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'pvpgn_bnet',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pvpgn_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customUser', to='authentication.PvpgnBnet', verbose_name='Пользователь PvPGN')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customUser', to=settings.AUTH_USER_MODEL, verbose_name='Реальный пользователь')),
            ],
        ),
    ]
