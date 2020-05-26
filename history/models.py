from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HistoryInput(models.Model):
    objects = models.Manager()

    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'history', null=True, default=None)  
    what = models.CharField(max_length=100)
    start = models.DateField(auto_now_add=False)
    end = models.CharField(max_length= 20, default="-ing")
    end_date = models.DateField(null=True, blank=True)
    end_ing = models.CharField(max_length=10, default="-ing")
    ing = models.BooleanField()
    # howmajorwasit = 
    desc = models.CharField(max_length=1000)

    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True)
    url = models.URLField(max_length=10000, blank=True)

    def __str__(self):
        return self.what