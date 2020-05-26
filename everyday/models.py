from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from emoji_picker.widgets import EmojiPickerTextInputAdmin

class NewEvent(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'event', null=True, default=None)
    when = models.DateField(_('When'), auto_now_add=False)
    end = models.DateField(_('End'), null=True)
    all_day = models.BooleanField(_('All day'), default=True)
    what = models.CharField(_('What'), max_length = 5000, default="None")

    kw1 = models.CharField(max_length=100, default="")
    kw2 = models.CharField(max_length=100, default="")
    kw3 = models.CharField(max_length=100, default="")
    emoji = models.CharField(max_length = 10, default="")
    # models.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        # ordering = ['-start']

    # 관리자 사이트에 표시될 객체 이름 설정 
    def __str__(self):
        return str(self.when)

class EverydayInput(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'everydayxxx', null=True, default=None)
    date = models.DateField(auto_now_add=True)

    # slug = models.SlugField(max_length=100, allow_unicode=True, blank=True)
    # url = models.URLField(max_length=10000, blank=True)

    contents = models.CharField(max_length=10485759, default="How was your day")
    # format_simple = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.date)

# class EverydayInputFree(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'everyday', null=True, default=None)
    date = models.DateField(auto_now_add=True)

    format_free = models.CharField(max_length=10485759)
    
    def __str__(self):
        return str(self.date)

# class EverydayInputiSimple(models.Model):
    objects = models.Manager()
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'everyday', null=True, default=None)
    date = models.DateField(auto_now_add=True)

    format_simple = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.date)
