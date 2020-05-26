from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):   # (UserCreationForm)이라는 건 그 form의 모든 property를 가져오겠다는 뜻.
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'all-inputs'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'all-inputs'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'all-inputs'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'all-inputs'}))


    class Meta:     # 이 RegisterForm에 있는 내용을 User Database에 저장하겠다는 class  
        model = User    # 여기에 저장을 할 때마다 "User"라는 model에 변화를 주겠다. 
        fields = ["username", "email", "password1", "password2"]
      
        # 위의 fields가 순서대로 나타남. 'email' 제외하고는 이미 UserCreationForm에 있으므로 위에서 안 적어줘도 괜찮다. 
