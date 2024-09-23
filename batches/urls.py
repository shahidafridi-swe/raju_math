from django.urls import path 
from . import views

urlpatterns = [
    path('', views.batches, name="batches" ),
    path('batch_details/<int:id>/', views.batchDetails, name="batch_details" ),
    path('add_batch/', views.add_batch, name='add_batch'),
    path('update_batch/<int:pk>/', views.update_batch, name='update_batch'),
    path('delete_batch/<int:pk>/', views.delete_batch, name='delete_batch'),
    path('batch/<int:batch_id>/attendance_day/<str:date>/', views.attendance_details, name='attendance_day_details'),
    path('batch/<int:batch_id>/attendance_day_update/<str:date>/', views.attendance_update, name='attendance_day_update'),
]
