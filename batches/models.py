from django.db import models
from students.models import Student
from core.models import CurrentClass

class Batch(models.Model):
    students = models.ManyToManyField(Student, null=True, blank=True, related_name="batches")
    title = models.CharField(max_length=255)
    level = models.ForeignKey(CurrentClass, on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=255, default='')
    time = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    fee = models.IntegerField()
    
    attendances = models.ManyToManyField('Attendance', blank=True, related_name="batches")
    
    def __str__(self) -> str:
        return self.title
    

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date = models.DateField()
    is_attend = models.BooleanField(default=False)  
    def __str__(self):
        return f"{self.student.user.first_name} - {self.batch.title} - {self.date} - {'Attended' if self.is_attend else 'Unattended'}"