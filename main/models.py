from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    objects = models.Manager()

    authuser = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'userinfo', null=True, default=None)  # UserInfo가 생성될 때마다 user에게 link된다!
    # 사용자의 이름 (실명)
    name = models.CharField(max_length=50)
    # 사용자의 한줄 소개
    introduction = models.TextField()
    # 아래는 소셜 미디어를 입력하는 부분입니다
    insta = models.CharField(max_length=1000, blank=True, default="https://hiim.kr/tong")
    facebook = models.CharField(max_length=1000, blank=True, default="https://hiim.kr/tong")
    linkedin = models.CharField(max_length=1000, blank=True, default="https://hiim.kr/tong")
    youtube = models.CharField(max_length=1000, blank=True, default="https://hiim.kr/tong")
    blog = models.CharField(max_length=1000, blank=True, default="https://hiim.kr/tong")
    others = models.CharField(max_length=1000, blank=True, default="https://hiim.kr/tong")

    def __str__(self):
        return self.name

