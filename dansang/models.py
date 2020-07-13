from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class DansangSet(models.Model):
    objects = models.Manager()

class DansangInput(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'dansang', null=True, default=None)
    title = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=False)
    modified = models.DateTimeField(auto_now=True)
    contents = models.CharField(max_length=100000)
    keyword = models.CharField(max_length=100, blank=True)
    first_sentence = models.CharField(max_length=100, blank=True)

    # image = models.ImageField(upload_to='')

    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True)
    url = models.CharField(max_length=10000, blank=True)

    def __str__(self):
        return (str(self.authuser)+"-----"+str(self.created)[:16])

class DansangSeed(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length = 100)
    subtitle = models.CharField(max_length = 100)
    url = models.URLField(max_length=10000)
    datePosted = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.title
