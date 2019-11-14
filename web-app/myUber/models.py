from django.db import models

# Create your models here.
class account(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    def __str__(self):
        return self.username

class driver(models.Model):
    user = models.OneToOneField(to=account, to_field='username', on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    license_number = models.CharField(max_length=20)
    space = models.IntegerField(default=0)
    special_info = models.CharField(max_length=20, default='None')
    def __str__(self):
        return self.username

class ride(models.Model):
    Status=(
        ('O','open'),
        ('D','during'),
        ('C','completed'),
    )
    id = models.AutoField(primary_key=True)
    dest = models.CharField(max_length=20)
    arrive_t = models.TimeField()
    v_type = models.CharField(max_length=20)
    special = models.CharField(max_length=20)
    number = models.IntegerField(default=1)
    s_num = models.IntegerField(default=0)
    shared = models.BooleanField(default=True)
    status = models.CharField(choices=Status, max_length=20)
    driver = models.CharField(max_length=20, null=True, blank=True)
    owner = models.CharField(max_length=20)
    sharer = models.CharField(max_length=20, null=True, blank=True)