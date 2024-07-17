from django.db import models
from students.models import Student


class Batch(models.Model):
    students = models.ManyToManyField(Student, null=True, blank=True, related_name="batches")
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    fee = models.IntegerField()
    
    def __str__(self) -> str:
        return self.title
    
