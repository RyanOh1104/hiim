from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):   # (UserCreationForm)이라는 건 그 form의 모든 property를 가져오겠다는 뜻.
    username = forms.CharField(widget=forms.TextInput(attrs={
        }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        }))

    class Meta:     # 이 RegisterForm에 있는 내용을 User Database에 저장하겠다는 class  
        model = User    # 여기에 저장을 할 때마다 "User"라는 model에 변화를 주겠다. 
        fields = ["username", "email", "password1", "password2"]
