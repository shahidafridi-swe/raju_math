from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test

def superuser_required(user):
    return user.is_superuser


@user_passes_test(superuser_required, login_url='home')
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



@user_passes_test(superuser_required, login_url='home')
def studentDetails(request, id):
    
    student = Student.objects.get(id=id)
    context = {
        "student" : student
    }
    return render(request, 'students/student_details.html', context)

@user_passes_test(superuser_required, login_url='home')
def addStudent(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student and user created successfully!')
            return redirect('students')  # Replace 'students_list' with the name of your desired redirect URL
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    
    return render(request, 'students/add_student.html', {'form': form})

