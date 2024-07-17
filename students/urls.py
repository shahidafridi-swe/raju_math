from django.urls import path
from . import views



urlpatterns = [
    path('',views.students, name="students"),
    path('student_details/<int:id>/',views.studentDetails, name="student_details"),
]
