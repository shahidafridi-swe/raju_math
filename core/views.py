from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Banner, SuccessStudent
from students.models import Student
from django.contrib.auth.decorators import login_required

def home(request):
    banners = Banner.objects.all()
    successStudents = SuccessStudent.objects.all()
    context = {
        'banners' : banners,
        'successStudents': successStudents
    }
    print(banners[0])
    return render(request, 'core/home.html', context)


def userLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"'{username}' logged in successfully")
                return redirect('home')
            else:
                messages.error(request, f"'{username}' user not found !!!")
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, "Your Password is incorrect !!!")
            except:
                messages.error(request, f"'{username}' user not found !!!")
    else:
        form = AuthenticationForm()           
    return render(request, 'core/login.html',{'form':form, 'type':'Login'})

 
@login_required(login_url='login')
def userProfile(request):
    user = request.user
    student = Student.objects.get(user=user)
    return render(request, 'core/profile.html', {"user": user, "student": student})

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'Logout successfull !!!')
    return redirect('login')


def setPassword(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully!!!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'core/login.html',{'form':form, 'type':'Change Password'})