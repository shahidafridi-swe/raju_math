from django import forms
from django.contrib.auth.models import User
from .models import Student,Payment
import datetime

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=11, required=True)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'image', 'school', 'subjects' ,'current_class', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Student Address'}),
            'subjects': forms.CheckboxSelectMultiple(),  # This will display the subjects as checkboxes
        }

    def save(self, commit=True):
        phone = self.cleaned_data['phone']
        existing_users = User.objects.filter(username__startswith=phone).count()
        if existing_users >= 5:
            raise forms.ValidationError("Student limit exceeded for this phone number.")
        
        username = f"{phone}{existing_users + 1}"
        user = User(
            username=username,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        user.set_password(phone)  # Set the phone number as the password
        if commit:
            user.save()

        student = super().save(commit=False)
        student.user = user
        student.joining_class = student.current_class.name  # Assuming current_class has a 'name' field
        if commit:
            student.save()
            self.save_m2m()  # Save many-to-many relationships
        return student



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'month', 'year']
        widgets = {
            'month': forms.Select(choices=Payment.MONTH_CHOICES),
            'year': forms.Select(choices=[(year, year) for year in range(2024, datetime.datetime.now().year + 2)])
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        if student:
            self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.filter(id=student.id), initial=student, widget=forms.HiddenInput())