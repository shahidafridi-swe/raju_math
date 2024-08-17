from django.db import models
from django.contrib.auth.models import User 
from core.models import CurrentClass
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.utils import timezone

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
      
    def payment_due_month_count(self):
        unpaid_month =Payment.objects.filter(student=self, is_paid=False).count()
        return unpaid_month

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_date = models.DateField(blank=True, null=True)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.month} {self.year}"
