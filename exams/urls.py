from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/details/', views.exam_details, name='exam_details'),
    path('<int:pk>/update/', views.exam_update, name='exam_update'),
]
