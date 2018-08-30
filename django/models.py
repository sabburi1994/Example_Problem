class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    objects = models.Manager()
    manager = AuthUserManager()


    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'auth_user'


class InstaData(models.Model):
    insta_name = models.CharField(primary_key=True, max_length=255, default='Benutzername')
    insta_password = models.CharField(max_length=255, default='Passwort')
    activate_bot = models.NullBooleanField(default=True)
    proxy_ip = models.TextField(blank=True, null=True)
    proxy_port = models.IntegerField(blank=True, null=True)
    is_beta_tester = models.NullBooleanField(null=True,default=False)
    # username = models.CharField(max_length=150)
    username = models.ForeignKey(AuthUser, default=1, on_delete=models.CASCADE)
    login_error = models.BooleanField(default = False)
    objects = models.Manager()

    def __str__(self):
        return self.insta_name
    # username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username', blank=True, null=True)


class FollowerLog(models.Model):
    insta_name = models.ForeignKey(InstaData, on_delete=models.CASCADE)
    log_time = models.DateTimeField(blank=True, null=True)
    follower_amount = models.IntegerField(blank=True, default=0)
    following_amount = models.IntegerField(blank=True, default=0)
    myquery = FollowerLogManager()

    def __str__(self):
        return self.insta_name
