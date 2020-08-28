from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class DansangInput(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'dansang', null=True, default=None)
    title = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=False)
    img = models.ImageField(null=True, blank=True, upload_to="dansang_img")
    contents = models.CharField(max_length=100000)
    category = models.CharField(max_length=100, default="미분류", null=True, blank=True)
    categoryEng = models.CharField(max_length=100, default="mibunryu", null=True, blank=True)

    keyword = models.CharField(max_length=100, blank=True)
    first_sentence = models.CharField(max_length=100, blank=True)

    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True)
    url = models.CharField(max_length=10000, blank=True)

    # Django Admin에 어떻게 보여질지를 설정하는 부분입니다.
    def __str__(self):
        return (str(self.authuser)+"-----"+str(self.created)[:16])

#############################################################################################################
########## 여기서부터는 '씨앗'이라는 feature에 관한 부분입니다. 당장 중요치 않으니 일단은 무시해주세요! ##########
#############################################################################################################

class SeedCategory(models.Model):
    objects = models.Manager()
    category = models.CharField(max_length=10, default="책")

    def __str__(self):
        return self.category

class SeedCategoryEng(models.Model):
    objects = models.Manager()
    category_eng = models.CharField(max_length=10, default="book")
    in_kor = models.ForeignKey(SeedCategory, on_delete=models.CASCADE, related_name = 'kor', null=True, default=None)

    def __str__(self):
        return self.category_eng

class DansangSeed(models.Model):
    objects = models.Manager()

    category_eng = models.ForeignKey(SeedCategoryEng, on_delete=models.CASCADE, related_name = 'rel_cat_eng', null=True, default=None) 
    category = models.ForeignKey(SeedCategory, on_delete=models.CASCADE, related_name = 'rel_cat_kor', null=True, default=None)
    title = models.CharField(max_length = 100)
    subtitle = models.CharField(max_length = 100)
    url = models.URLField(max_length=10000)
    datePosted = models.DateField(auto_now_add=False)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.title


