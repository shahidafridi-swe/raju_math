from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userLogin, name='login'),
    path('profile/', views.userProfile, name='profile'),
    path('logout/', views.logoutUser, name="logout"),
    path('set_password/', views.setPassword, name="set_password"),
     
]
