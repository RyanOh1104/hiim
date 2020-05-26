from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import HistoryInput
from django.utils import timezone
from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput

class HistoryInputForm(forms.ModelForm):
    what = forms.CharField(widget=forms.TextInput(
        attrs={'style':'font-size: 30px', 'placeholder':'왓'}
    ))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'간단하게 설명해주세요!'}
    ))

    class Meta:
        model=HistoryInput
        fields=['what', 'start', 'end_date', 'ing', 'desc']
        widgets = {
            'authuser':forms.HiddenInput(),
            'start': MonthPickerInput(
                options={'format':'YYYY-MM-01', 'locale':'ko'}
            ),
            'end_date': MonthPickerInput(
                options={'format':'YYYY-MM-01', 'locale':'ko'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super(HistoryInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['end_date'].required = False

