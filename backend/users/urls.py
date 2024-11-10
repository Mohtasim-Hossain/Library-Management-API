from django.urls import path
from .views import HomeView, RegisterView, LoginView, AdminView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin-dashboard/', AdminView.as_view(), name='admin_dashboard'),
]
