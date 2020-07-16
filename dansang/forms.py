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
    img = forms.ImageField(required=False)

    class Meta:
        model=DansangInput
        fields=['title', 'img', 'subtitle', 'contents']
        widgets = {
            'authuser':forms.HiddenInput(), 
            'first_sentence':forms.HiddenInput(),
            'url' : forms.HiddenInput(),
            'slug' : forms.HiddenInput(),
            'contents': SummernoteInplaceWidget()
        }
    
    def __init__(self, *args, **kwargs):
        super(DansangInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtitle'].required = False