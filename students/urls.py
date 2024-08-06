from django.urls import path
from . import views



urlpatterns = [
    path('',views.students, name="students"),
    path('student_details/<int:id>/',views.studentDetails, name="student_details"),
    path('add/',views.addStudent, name="add_student"),
    path('payment/<int:student_id>/', views.payment_view, name='payment_view'),
]
