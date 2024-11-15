"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from users.views import LoginView, RegisterView, AdminView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('books.admin_urls')), 
    # path('login/', LoginView.as_view(), name='login'),  # Path for user login
    # path('register/', RegisterView.as_view(), name='register'),  # Path for user registration
    # path('admin-dashboard/', AdminView.as_view(), name='admin-dahsboard'),  # Path for user registration
    path('', include('users.urls')),
    path('books/', include('books.urls')),
]
