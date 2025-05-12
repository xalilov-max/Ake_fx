from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard, register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
