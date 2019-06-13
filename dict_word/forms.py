from django import forms

from .models import YoudaoResult

class SearchForm(forms.ModelForm):

    class Meta:
        model = YoudaoResult
        fields = {
            'word'
        }