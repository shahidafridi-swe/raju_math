from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Exam, StudentExamMark

@receiver(post_save, sender=Exam)
def create_exam_marks(sender, instance, created, **kwargs):
    if created:
        batch = instance.batch
        students = batch.students.all()
        for student in students:
            StudentExamMark.objects.create(student=student, exam=instance)
