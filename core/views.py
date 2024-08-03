from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Banner, SuccessStudent, NoticeBoard
from students.models import Student
from django.contrib.auth.decorators import login_required
from .forms import NoticeBoardForm

def home(request):
    banners = Banner.objects.all()
    successStudents = SuccessStudent.objects.all()
    notice = NoticeBoard.objects.latest('last_update')  # Assuming you want to show the latest notice
    form = NoticeBoardForm(instance=notice)

    context = {
        'banners': banners,
        'successStudents': successStudents,
        'notice': notice,
        'form': form
    }
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
    try:
        student = Student.objects.get(user=user)
    except:
        student = None
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
    return render(request, 'core/change_password.html',{'form':form, 'type':'Change Password'})


def noticeUpdate(request, pk):
    notice = get_object_or_404(NoticeBoard, pk=pk)
    form = NoticeBoardForm(instance=notice)

    if request.method == 'POST':
        form = NoticeBoardForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
        'notice': notice
    }
    return render(request, 'core/home.html', context)