from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=11, required=True)

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'image', 'school_name', 'joining_class', 'current_class', 'address']
        
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Student Address'})
        }  

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['phone'])  # Set the phone number as the password
        if commit:
            user.save()
        
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if User.objects.filter(username=username).exists():
            self.add_error('username', "Username is already taken")

       