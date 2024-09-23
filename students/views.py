from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Student, Payment
from .forms import StudentForm, PaymentForm
from django.db.models import Q, Count
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django import forms
import datetime
from django.utils import timezone

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
            Q(school__name__icontains=search_query) |  # Correct usage
            Q(current_class__name__icontains=search_query)  # Correct usage
        )
    else:
        students = Student.objects.all()
     # Annotate each student with the count of distinct unpaid months
    students = students.annotate(
        unpaid_months_count=Count('payment__month', filter=Q(payment__is_paid=False), distinct=True)
    )
    context = {
        'students': students,
        'search_query': search_query
    }
    
    return render(request, 'students/students_list.html', context)



@user_passes_test(superuser_required, login_url='home')
def studentDetails(request, id):
    cur_month = datetime.datetime.now().month
    cur_year = datetime.datetime.now().year
    student = get_object_or_404(Student, id=id)
    form = PaymentForm()
    payments = Payment.objects.filter(student=student).order_by('year', 'month')
    context = {
        "student": student,
        "month": cur_month,
        "year": cur_year,
        "form": form,
        "payments": payments
    }
    return render(request, 'students/student_details.html', context)


@user_passes_test(superuser_required, login_url='home')
def addStudent(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Student and user created successfully!')
                return redirect('students')  # Replace 'students' with the name of your desired redirect URL
            except forms.ValidationError as e:
                form.add_error(None, e)
                messages.error(request, 'Student limit exceeded for this phone number.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    
    return render(request, 'students/add_student.html', {'form': form})


def pay_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.is_paid = True  # Mark payment as paid
            payment.save()  # Save the updated payment instance
            messages.success(request, 'Payment recorded successfully!')
            return redirect('student_details', id=payment.student.id)
        else:
            print(form.errors)
            messages.error(request, 'Failed to record payment. Please check the details.')
    else:
        form = PaymentForm(instance=payment)

    return render(request, 'students/student_details.html', {'form': form, 'payment': payment})


def payments_list(request):
    if request.user.is_superuser:
        payments = Payment.objects.filter(is_paid=True).order_by('-payment_date')
    else:
        student = getattr(request.user, 'student', None)
        if student is not None:
            payments = Payment.objects.filter(student=student)
        else:
            payments = []  # Handle case where the user is not a student and not a superuser

    return render(request, 'students/payments_list.html', {'payments': payments})
