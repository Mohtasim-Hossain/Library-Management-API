# books/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Book
# from users.models import BorrowedBook
from django.apps import apps

BorrowedBook = apps.get_model('users', 'BorrowedBook')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'published_date', 'isbn', 'description', 'available']
        read_only_fields = ['isbn', 'title', 'author', 'published_date']


class BookDetailSerializer(serializers.ModelSerializer):
    current_borrower = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'published_date', 'isbn', 'description', 'available', 'current_borrower']
        

    def get_current_borrower(self, obj):
        # Filter for books that are currently borrowed and not yet returned
        borrowed_book = BorrowedBook.objects.filter(book=obj, return_deadline__gte=timezone.now().date()).first()
        if borrowed_book:
            return borrowed_book.user.username
        return None
