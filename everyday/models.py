from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from emoji_picker.widgets import EmojiPickerTextInputAdmin

class NewEvent(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'event', null=True, default=None)
    when = models.DateField(_('When'), auto_now_add=False)
    what = models.CharField(_('What'), max_length = 5000, default="None")
    # img = models.ImageField(null=True, blank=True, upload_to="everyday_img")

    kw1 = models.CharField(max_length=100)
    kw2 = models.CharField(max_length=100)
    kw3 = models.CharField(max_length=100)
    emoji = models.CharField(max_length = 100, default="", blank=True)

    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True)
    url = models.URLField(max_length = 1000, blank=True)
    # models.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])
    
    class Meta:
        verbose_name = _('Everyday')
        verbose_name_plural = _('Everydays')
        # ordering = ['-start']

    # 관리자 사이트에 표시될 객체 이름 설정 
    def __str__(self):
        # return str(self.when)
        # when-admin = str(self.when)[:15]
        return (str(self.authuser)+"-----"+str(self.when)[:15])

    # objects = models.Manager()
    # authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'everyday', null=True, default=None)
    # date = models.DateField(auto_now_add=True)

    # format_simple = models.CharField(max_length=200)
    
    # def __str__(self):
    #     return str(self.date)
