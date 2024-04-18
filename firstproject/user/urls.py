from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('verifyemail/',views.verifyemail, name='verifyemail'),
    path('setpassword/',views.setpassword, name='setpassword'),
    path('dashboard/',views.dashboard, name='dashboard')

]