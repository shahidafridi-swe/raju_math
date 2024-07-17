from django.urls import path 
from . import views

urlpatterns = [
    path('', views.batches, name="batches" ),
    path('batch/<int:id>/', views.batchDetails, name="batch_details" ),
    path('add/', views.add_batch, name='add_batch'),
]
