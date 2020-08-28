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
        attrs={
            'style':'font-size: 44px; border: none;', 
            'placeholder':'제목'}))
    subtitle = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'style':'font-size: 17px; border: none;', 
            'placeholder':'부제목이 있으면 입력해주세요!'}))
    img = forms.ImageField(required=False)
    category = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'style':'font-size: 17px; border: none;',
            'placeholder':'#새 카테고리'}))

    class Meta:
        model=DansangInput
        fields=['title', 'img', 'subtitle', 'contents', 'category']
        widgets = {
            'contents': SummernoteInplaceWidget()
        }
    
    # 각 필드의 레이블을 없애주는 부분입니다. 
    def __init__(self, *args, **kwargs):
        super(DansangInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False