from django import forms
from django.utils import timezone
from .models import Batch,Attendance

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ('title', 'level', 'day', 'time', 'fee')
        


class AttendanceDateForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=timezone.now)
    
class AttendanceUpdateForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date']

    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

