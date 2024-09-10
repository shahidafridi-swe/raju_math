# forms.py
from django import forms
from .models import Exam, StudentExamMark


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title']
        
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Exam Title'

class StudentMarksForm(forms.ModelForm):
    class Meta:
        model = StudentExamMark
        fields = ['marks']

    def __init__(self, *args, **kwargs):
        super(StudentMarksForm, self).__init__(*args, **kwargs)
        # Set the label of the 'marks' field to an empty string
        self.fields['marks'].label = ''
