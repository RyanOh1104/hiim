from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    objects = models.Manager()

    authuser = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'userinfo', null=True, default=None)  # UserInfo가 생성될 때마다 user에게 link된다!
    name = models.CharField(max_length=50)
    # background = models.CharField(max_length=40)
    introduction = models.TextField()
    insta = models.CharField(max_length=1000)
    facebook = models.CharField(max_length=1000)
    linkedin = models.CharField(max_length=1000)
    youtube = models.CharField(max_length=1000)
    blog = models.CharField(max_length=1000)
    others = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
