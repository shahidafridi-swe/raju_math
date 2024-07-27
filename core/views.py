from django.shortcuts import render
from .models import Banner, SuccessStudent


def home(request):
    banners = Banner.objects.all()
    successStudents = SuccessStudent.objects.all()
    context = {
        'banners' : banners,
        'successStudents': successStudents
    }
    print(banners[0])
    return render(request, 'core/home.html', context)
