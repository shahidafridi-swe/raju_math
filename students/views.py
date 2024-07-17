# views.py
from django.shortcuts import render
from .models import Student
from django.db.models import Q

def students(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        students = Student.objects.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(school_name__icontains=search_query) |
            Q(current_class__icontains=search_query)
        )
    else:
        students = Student.objects.all()
    
    context = {
        'students': students,
        'search_query': search_query
    }
    
    return render(request, 'students/students_list.html', context)



def studentDetails(request, id):
    
    student = Student.objects.get(id=id)
    context = {
        "student" : student
    }
    return render(request, 'students/student_details.html', context)