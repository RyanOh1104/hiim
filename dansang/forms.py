from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import DansangInput
from django.utils import timezone
from crispy_forms.helper import FormHelper
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

class DansangInputForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'style':'font-size: 44px; background-color: #f6f5f1; border: none;', 
        'placeholder':'제목'}))
    subtitle = forms.CharField(widget=forms.TextInput(
        attrs={'style':'font-size: 17px; background-color: #f6f5f1; border: none;', 
        'placeholder':'부제목이 있으면 입력해주세요!'}))
    # contents = SummernoteTextField()
    # source = forms.CharField(widget=forms.TextInput(
    #     attrs={'style':'font-size: 13px; background-color: #f6f5f1; border: none; border-bottom: 1px solid rgba(0, 0, 0, 0.125);',
    #     'placeholder':'무엇을 보고 이런 생각을 했는지 url을 공유해줄 수 있나요?'
    #     }))
    class Meta:
        model=DansangInput
        fields=['title', 'subtitle', 'contents', 'keyword']
        widgets = {
            'authuser':forms.HiddenInput(), 
            'first_sentence':forms.HiddenInput(),
            'contents': SummernoteInplaceWidget()
        }
    
    def __init__(self, *args, **kwargs):
        super(DansangInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtitle'].required = False