from django.db import models
from django.contrib.auth.models import User
from authentication.passhash import makeHash

# Create your models here.

#Manager for PvPGN profile creation
#It's necessary because PvPGN model is not Django created model
class PvpgnBnetManager(models.Manager):
    def createProfile(self, name, password, email, isAdmin='false'):
        newID = PvpgnBnet.objects.count()
        newProfile = self.create(uid=newID,
            acct_username = name,
            username = name,
            acct_userid=newID,
            acct_passhash1 = makeHash(password),
            acct_email = email,
            auth_admin = isAdmin,
            auth_normallogin = "true",
            auth_changepass = "true",
            auth_changeprofile = "true",
            auth_botlogin = "false",
            auth_operator = "false",
            new_at_team_flag = 0,
            auth_lock = "false",
            auth_locktime = 0,
            auth_lockreason = None,
            auth_mute = "false",
            auth_mutetime = 0,
            auth_mutereason = None,
            auth_command_groups = 1,
            acct_lastlogin_time = 0,
            acct_lastlogin_owner = "Panky",
            acct_lastlogin_clienttag = "D2XP",
            acct_lastlogin_ip = "192.168.1.14",
            acct_ctime = "0")
        return newProfile


#Model of PvPGN Profile (this table created by PvPGN Server so there is many PvPGN fields)
class PvpgnBnet(models.Model):
    uid = models.IntegerField(primary_key=True, null=False, blank=False, editable=True)
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

    objects = PvpgnBnetManager()

    class Meta:
        managed = False
        db_table = 'pvpgn_bnet'


#Model of user on the site (it contains relation between Django user and PvPGN profile)
class CustomUser(models.Model):
    user = models.OneToOneField(verbose_name="Реальный пользователь", to=User, on_delete=models.CASCADE,
                                related_name="customUser")
    pvpgn_user = models.OneToOneField(verbose_name="Пользователь PvPGN", to=PvpgnBnet, on_delete=models.CASCADE,
                                      related_name="customUser")
    photo = models.ImageField(verbose_name="Аватар пользователя", upload_to='Avatars',
                              default='Avatars/blankAvatar/blankAvatar.png')
