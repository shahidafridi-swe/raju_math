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
    
    def __str__(self) -> str:
        return self.title
    
