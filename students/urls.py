from django.urls import path
from . import views



urlpatterns = [
    path('',views.students, name="students"),
    path('student_details/<int:id>/',views.studentDetails, name="student_details"),
    path('add/',views.addStudent, name="add_student"),
    path('payment/<int:payment_id>/', views.pay_payment, name='pay_payment'),
    path('payments_list/', views.payments_list, name='payments_list'),
]
