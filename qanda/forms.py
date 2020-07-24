from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Question, Answer
from crispy_forms.helper import FormHelper
from django.utils import timezone

class AnswerForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : 4,
        'class' : 'answerInput',
        }))

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model=Answer
        fields=['answer',]
        widgets = {
            # 'authuser':forms.HiddenInput(), 
        }