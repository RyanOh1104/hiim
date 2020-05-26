from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, formset_factory
from .models import EverydayInput, NewEvent
from django.utils import timezone
from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput
from emoji_picker.widgets import EmojiPickerTextInputAdmin


# class EverydayInputForm(forms.ModelForm):
#     contents = forms.CharField(required=False, 
#     widget = forms.Textarea(attrs={
#         'placeholder': '장문으로 쓰기가 부담스럽다면, 한 줄씩 써보는 건 어때요?',
#         'rows' : 8
#         }))

#     def __init__(self, *args, **kwargs):
#         super(EverydayInputForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_show_labels = False

#     class Meta:
#         model=EverydayInput
#         fields=['contents']
#         widgets = {
#             'authuser':forms.HiddenInput(),
#         }

class EEverydayInputForm(forms.ModelForm):
    what = forms.CharField(required=False, 
    widget = forms.Textarea(attrs={
        'placeholder': '장문으로 쓰기가 부담스럽다면, 한 줄씩 써보는 건 어때요?',
        'rows' : 8
        }))
    kw1 = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder' : '하나', 'rows' : 1
    }))
    kw2 = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder' : '둘', 'rows' : 1
    }))
    kw3 = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder' : '셋', 'rows' : 1
    }))
    emoji = forms.CharField(required=False, widget=EmojiPickerTextInputAdmin(attrs={
        'class' : 'emojis'
    }))

    def __init__(self, *args, **kwargs):
        super(EEverydayInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    # when이 date picker인데 everydayinput에서 입력하면 데이터가 입력되지 않았다고 나온다!!!
    class Meta:
        model=NewEvent
        fields=['when', 'what', 'kw1', 'kw2', 'kw3', 'emoji']
        widgets = {'authuser':forms.HiddenInput(),
        'all_day':forms.HiddenInput(),
        'when' : MonthPickerInput(
            options={'format':'YYYY-MM-DD', 'locale':'ko'}
            )
        }


