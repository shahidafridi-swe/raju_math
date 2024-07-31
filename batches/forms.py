from django import forms

from .models import Batch

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ('title', 'level', 'day', 'time', 'fee')