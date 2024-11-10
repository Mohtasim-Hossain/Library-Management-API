# books/admin_urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookAdminViewSet

# Define the router for admin-specific routes
router = DefaultRouter()
router.register(r'books', BookAdminViewSet, basename='admin-books')

urlpatterns = router.urls


