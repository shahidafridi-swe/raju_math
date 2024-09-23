from django.shortcuts import render, redirect,get_object_or_404
from .models import Batch, Attendance
from .forms import BatchForm, AttendanceDateForm, AttendanceUpdateForm
from students.models import Student
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from exams.models import Exam, StudentExamMark
from exams.forms import ExamForm

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
    batch = get_object_or_404(Batch, id=id)
    search_query = request.GET.get('search_query', '')

    # Handle student search
    if search_query:
        students = Student.objects.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(school__name__icontains=search_query) |
            Q(current_class__name__icontains=search_query)
        ).distinct()
    else:
        students = None

    exams = Exam.objects.filter(batch=batch)

    if request.method == 'POST':
        if 'student_id' in request.POST:
            # Adding student to batch
            student_id = request.POST.get('student_id')
            student = Student.objects.get(id=student_id)
            batch.students.add(student)
            return redirect('batch_details', id=batch.id)

        elif 'date' in request.POST:
            # Handling attendance form submission
            attendance_form = AttendanceDateForm(request.POST)
            if attendance_form.is_valid():
                date = attendance_form.cleaned_data['date']

                # Check if attendance for the given date and batch already exists
                if Attendance.objects.filter(batch=batch, date=date).exists():
                    messages.error(request, f"Attendance for {date} has already been added for this batch.")
                else:
                    # Create attendance entries for each student in the batch
                    for student in batch.students.all():
                        Attendance.objects.create(student=student, batch=batch, date=date, is_attend=False)
                    messages.success(request, f"Attendance for {date} added successfully.")
                
                return redirect('batch_details', id=batch.id)

        else:
            # Handling exam form submission
            exam_form = ExamForm(request.POST)
            if exam_form.is_valid():
                new_exam = exam_form.save(commit=False)
                new_exam.batch = batch
                new_exam.save()
                return redirect('batch_details', id=batch.id)
    else:
        attendance_form = AttendanceDateForm()
        exam_form = ExamForm()
    attendances = Attendance.objects.filter(batch=batch)
    context = {
        'students': students,
        'search_query': search_query,
        'batch': batch,
        'exams': exams,
        'exam_form': exam_form,
        'attendances':attendances,
        'attendance_form': attendance_form,  # Pass the attendance form
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
        'form': form,
        'type': 'ADD'
    }
    return render(request, 'batches/batch_form.html', context)


@user_passes_test(superuser_required, login_url='home')
def update_batch(request, pk):
    batch = Batch.objects.get(id=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            batch = form.save()
            messages.success(request, f"'{batch.title}' updated successfully")
            return redirect('batches')  # Redirect to the list of batches
    else:
        form = BatchForm(instance=batch)
    
    context = {
        'form': form,
        'type': 'UPDATE',
        'batch': batch  # Make sure the batch is included in the context
    }
    return render(request, 'batches/batch_form.html', context)

@user_passes_test(superuser_required, login_url='home')
def delete_batch(request, pk):
    batch = get_object_or_404(Batch, id=pk)
    if request.method == 'POST':
        batch.delete()
        messages.success(request, f"'{batch.title}' deleted successfully")
        return redirect('batches')  # Redirect to the list of batches
    
    context = {
        'batch': batch
    }
    return render(request, 'batches/batch_confirm_delete.html', context)

