from django.db import models

from batches.models import Batch
from students.models import Student

class Exam(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} - {self.batch}"


class StudentExamMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.CharField(max_length=10, blank=True, null=True)  # Marks out of 100 or other range

    def __str__(self):
        return f"{self.student.user.username} - {self.exam.title} - {self.marks}"