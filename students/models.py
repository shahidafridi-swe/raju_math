from django.db import models
from django.contrib.auth.models import User 
from core.models import CurrentClass
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class School(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    image = models.ImageField(upload_to='students/images', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    subjects = models.ManyToManyField(Subject, blank=True, related_name="students")
    joining_class = models.CharField(max_length=10, blank=True, null=True)
    current_class = models.ForeignKey(CurrentClass, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.username   
      
   

class Payment(models.Model):
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(datetime.datetime.now().year + 1)])

    def __str__(self) -> str:
        return f'{self.student.user.username} - {self.amount} - {self.get_month_display()}/{self.year}'

    def get_month_display(self):
        return dict(self.MONTH_CHOICES).get(self.month)
