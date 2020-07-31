from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import AllQuestion, Answer
from crispy_forms.helper import FormHelper
from django.utils import timezone

class AnswerForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : 3,
        'class' : 'answerInput',
        }))

    class Meta:
        model=Answer
        fields=['answer',]
