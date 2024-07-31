from django.shortcuts import render, redirect
from .models import Batch
from .forms import BatchForm
from students.models import Student
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required, login_url='home')
def batches(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        batches = Batch.objects.filter(
            Q(title__icontains=search_query) |
            Q(day__icontains=search_query) |
            Q(time__icontains=search_query) |
            Q(level__icontains=search_query)
        )
    else:
        batches = Batch.objects.all()

    context = {
        'batches': batches,
        'search_query': search_query
    }
    return render(request, 'batches/batches.html', context)


@user_passes_test(superuser_required, login_url='home')
def batchDetails(request, id):
    batch = Batch.objects.get(id=id)
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
        students = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            student = Student.objects.get(id=student_id)
            batch.students.add(student)
            batch.save()
            return redirect('batch_details', id=batch.id)

    context = {
        'students': students,
        'search_query': search_query,
        "batch": batch
    }
   
    return render(request, "batches/batch_details.html", context)

@user_passes_test(superuser_required, login_url='home')
def add_batch(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch=form.save()
            messages.success(request, f"'{batch.title}' added successfully")
            return redirect('batches')  # Redirect to the list of batches
    else:
        form = BatchForm()
    
    context = {
        'form': form
    }
    return render(request, 'batches/batch_form.html', context)