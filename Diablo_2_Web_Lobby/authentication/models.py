from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PvpgnBnet(models.Model):
    uid = models.IntegerField(primary_key=True)
    acct_username = models.CharField(max_length=32, blank=True, null=True)
    username = models.CharField(unique=True, max_length=32, blank=True, null=True)
    acct_userid = models.IntegerField(blank=True, null=True)
    acct_passhash1 = models.CharField(max_length=40, blank=True, null=True)
    acct_email = models.CharField(max_length=128, blank=True, null=True)
    auth_admin = models.CharField(max_length=6, blank=True, null=True)
    auth_normallogin = models.CharField(max_length=6, blank=True, null=True)
    auth_changepass = models.CharField(max_length=6, blank=True, null=True)
    auth_changeprofile = models.CharField(max_length=6, blank=True, null=True)
    auth_botlogin = models.CharField(max_length=6, blank=True, null=True)
    auth_operator = models.CharField(max_length=6, blank=True, null=True)
    new_at_team_flag = models.IntegerField(blank=True, null=True)
    auth_lock = models.CharField(max_length=6, blank=True, null=True)
    auth_locktime = models.IntegerField(blank=True, null=True)
    auth_lockreason = models.CharField(max_length=128, blank=True, null=True)
    auth_mute = models.CharField(max_length=6, blank=True, null=True)
    auth_mutetime = models.IntegerField(blank=True, null=True)
    auth_mutereason = models.CharField(max_length=128, blank=True, null=True)
    auth_command_groups = models.CharField(max_length=16, blank=True, null=True)
    acct_lastlogin_time = models.IntegerField(blank=True, null=True)
    acct_lastlogin_owner = models.CharField(max_length=128, blank=True, null=True)
    acct_lastlogin_clienttag = models.CharField(max_length=4, blank=True, null=True)
    acct_lastlogin_ip = models.CharField(max_length=16, blank=True, null=True)
    acct_ctime = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pvpgn_bnet'


class CustomUser(models.Model):
    user = models.OneToOneField(verbose_name="Реальный пользователь", to=User, on_delete=models.CASCADE,
                                related_name="customUser")
    pvpgn_user = models.OneToOneField(verbose_name="Пользователь PvPGN", to=PvpgnBnet, on_delete=models.CASCADE,
                                      related_name="customUser")

