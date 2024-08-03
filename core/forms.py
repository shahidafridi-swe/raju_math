from .models import NoticeBoard
from django import forms

class NoticeBoardForm(forms.ModelForm):
    class Meta:
        model = NoticeBoard
        fields = ['notice']

    def __init__(self, *args, **kwargs):
        super(NoticeBoardForm, self).__init__(*args, **kwargs)

        self.fields['notice'].widget.attrs.update({'class': 'form-control'})