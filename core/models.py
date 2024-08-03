from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to='banners')
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title


class SuccessStudent(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='success_students', blank=True, null=True)
    school = models.CharField(max_length=255)
    current_class = models.CharField(max_length=50)
    success = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
    
class NoticeBoard(models.Model):
    notice = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
   