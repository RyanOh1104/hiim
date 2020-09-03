from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserInfo
# 아래 두개는 굳이 필요한 건지는 모르겠음
from django.contrib.auth.forms import UserCreationForm

class InputUserForm(forms.ModelForm):

    name = forms.CharField(label="이름", max_length=30, 
    widget=forms.TextInput(attrs={
        'placeholder': '반드시 실명!',
        # 'class':'all-inputs'
        }))
    
    # background = forms.CharField(label = "현재 소속" , max_length=40, 
    # widget=forms.TextInput(attrs={'placeholder': '현재 학교/직장 혹은 전공/직책 등을 간략하게 적어주세요!'}))

    introduction = forms.CharField(label = "저는,", max_length=60,
    widget=forms.Textarea(attrs={
        'placeholder': "'나'를 한 줄로 간략하게 표현해주세요!", 
        'rows':1, 
        # 'class':'all-inputs'
        }))

    insta = forms.CharField(label = "인스타그램", max_length=1000, required=False,
    widget=forms.TextInput(attrs={
        'placeholder': '계정을 적어주세요!', 
        # 'class':'all-inputs'
    }))

    facebook = forms.CharField(label = "페이스북", max_length=1000, required=False,
    widget=forms.TextInput(attrs={
        'placeholder': '프로필 링크를 복사하여 적어주세요!', 
        # 'class':'all-inputs'
    }))

    linkedin = forms.CharField(label = "링크드인", max_length=1000, required=False,
    widget=forms.TextInput(attrs={
        'placeholder': '프로필 링크를 복사하여 적어주세요!', 
        # 'class':'all-inputs'
    }))

    youtube = forms.CharField(label = "유튜브", max_length=1000, required=False,
    widget=forms.TextInput(attrs={
        'placeholder': '채널 링크를 복사하여 적어주세요!', 
        # 'class':'all-inputs'
    }))

    blog = forms.CharField(label = "블로그/브런치", max_length=1000, required=False,
    widget=forms.TextInput(attrs={
        'placeholder': '링크를 복사하여 적어주세요!', 
        # 'class':'all-inputs'
    }))

    others = forms.CharField(label = "+그 외", max_length=1000, required=False,
    widget=forms.TextInput(attrs={
        'placeholder': '링크를 복사하여 적어주세요!', 
        # 'class':'all-inputs'
    }))

    class Meta:
        model = UserInfo
        fields = ('name', 'introduction', 'insta', 'facebook', 'linkedin', 'youtube', 'blog', 'others')
        # fields 이렇게 하거나 전부다 하려면 그냥 '__all__' 하면 됨. 따옴표 넣어서.
