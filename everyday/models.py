from django.db import models
from django.utils.translation import ugettext_lazy as _ # 이건 뭐지?
from django.contrib.auth.models import User
from django.utils import timezone
from emoji_picker.widgets import EmojiPickerTextInputAdmin  # 원래 이모지를 넣을 때 별도의 emojiPicker를 썼는데, 지금은 일단 필요 없습니다!

class NewEvent(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'event', null=True, default=None)
    when = models.DateField(_('When'), auto_now_add=False)  # 날짜
    what = models.CharField(_('What'), max_length = 5000, default="None")   # 회고 내용

    # 아래는 사용자가 원하면 업로드하는 이미지입니다.
    img1 = models.ImageField(null=True, blank=True, upload_to="everyday_img")
    img2 = models.ImageField(null=True, blank=True, upload_to="everyday_img")
    img3 = models.ImageField(null=True, blank=True, upload_to="everyday_img")

    # 아래는 사용자가 입력하는 키워드와 이모지예요.
    kw1 = models.CharField(max_length=100)
    kw2 = models.CharField(max_length=100)
    kw3 = models.CharField(max_length=100)
    emoji = models.CharField(max_length = 100, default="", blank=True)

    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True)
    url = models.URLField(max_length = 1000, blank=True)
    
    # Admin 페이지에 보여질 이름이에요. 중요 X!
    class Meta:
        verbose_name = _('Everyday')
        verbose_name_plural = _('Everydays')

    # Admin 페이지에 표시될 객체 이름 설정입니다
    def __str__(self):
        return (str(self.authuser)+"-----"+str(self.when)[:15])

