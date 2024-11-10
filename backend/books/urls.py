# books/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookListView, BookDetailView, BorrowBookView, ReturnBookView, BookAdminViewSet

# router = DefaultRouter()
# router.register(r'admin/books', BookAdminViewSet, basename='admin-books')

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<str:title>/', BookDetailView.as_view(), name='book-detail'),
    path('<str:title>/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('<str:title>/return/', ReturnBookView.as_view(), name='return-book'),
    # path('', include(router.urls)),  # Register admin routes for CRUD operations
]
