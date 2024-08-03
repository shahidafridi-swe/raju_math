from django.db import models
from django.contrib.auth.models import User 

class School(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    image = models.ImageField(upload_to='students/images', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    joining_class = models.CharField(max_length=10, blank=True, null=True)
    current_class = models.CharField(max_length=10)
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
    amount = models.IntegerField()
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.student.user.username} - {self.amount} - {self.month}/{self.year}'