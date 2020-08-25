from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, formset_factory
from .models import NewEvent
from django.utils import timezone
from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput
# from emoji_picker.widgets import EmojiPickerTextInputAdmin

class EverydayInputForm(forms.ModelForm):
    what = forms.CharField(required=False, 
    widget = forms.Textarea(attrs={
        'rows' : 8,
        'class' : 'detail-contents'
        }))

    img1 = forms.ImageField(required=False)
    img2 = forms.ImageField(required=False)
    img3 = forms.ImageField(required=False)

    kw1 = forms.CharField(required=False, widget=forms.TextInput(attrs={
    'placeholder' : '하나', 'class' : 'keywords'
    }))
    kw2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
    'placeholder' : '둘', 'class' : 'keywords'
    }))
    kw3 = forms.CharField(required=False, widget=forms.TextInput(attrs={
    'placeholder' : '셋', 'class' : 'keywords'
    }))
    emoji = forms.CharField(required=False, widget=forms.TextInput(attrs={
    'placeholder':'', 'class' : 'emoji'
    }))

    ########## 여기는 왜 했는지 기억이 안 나네요..... ##########
    def __init__(self, *args, **kwargs):
        super(EverydayInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
    ##########################################################

    class Meta:
        model=NewEvent
        fields=['when', 'what', 'img1', 'img2', 'img3', 'kw1', 'kw2', 'kw3', 'emoji']
        widgets = {
        # 'authuser' : forms.HiddenInput(),
        'when' : MonthPickerInput(
            options={'format':'YYYY-MM-DD', 'locale':'ko'}
            )
        }



