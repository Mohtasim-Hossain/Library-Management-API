# books/views.py
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import Book
from .serializers import BookSerializer, BookDetailSerializer
# from users.models import BorrowedBook
from django.apps import apps

BorrowedBook = apps.get_model('users', 'BorrowedBook')



class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'title'  # Retrieve book by title instead of ID



class BorrowBookView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'title'  # Borrow book by title

    def post(self, request, title):
        book = self.get_object()

        # Check if the user is a member
        if not request.user.is_member():
            raise ValidationError("Only members can borrow books.")

        # Check if the book is available
        if not book.available:
            # Check if the user has already borrowed this book
            borrowed_book = BorrowedBook.objects.filter(user=request.user, book=book).first()
            if borrowed_book:
                return Response({
                    "message": f"You have already borrowed '{book.title}'."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            raise ValidationError("This book is currently not available for borrowing.")

        # Check if the user has reached their borrowing limit
        if not request.user.can_borrow_more_books():
            raise ValidationError("You have reached your borrowing limit.")

        # Mark the book as borrowed by setting available to False
        book.available = False
        book.save()

        # Create a BorrowedBook record with a return deadline
        return_deadline = timezone.now().date() + timezone.timedelta(days=14)  # 14-day borrowing period
        BorrowedBook.objects.create(
            user=request.user,
            book=book,
            borrow_date=timezone.now().date(),
            return_deadline=return_deadline
        )

        # Update the user's current borrowed books count
        request.user.current_borrowed_books += 1
        request.user.save()

        return Response({"message": f"You have successfully borrowed '{book.title}'."}, status=status.HTTP_200_OK)


class ReturnBookView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'title'  # Return book by title

    def post(self, request, title):
        book = self.get_object()

        # Check if the user has borrowed this book
        borrowed_book = BorrowedBook.objects.filter(user=request.user, book=book).first()
        if not borrowed_book:
            raise ValidationError("You have not borrowed this book.")

        # Calculate fine if the book is overdue
        fine = borrowed_book.calculate_fine()

        # Update book status to available
        book.available = True
        book.save()

        # Remove the BorrowedBook record (or mark it as returned if tracking history)
        borrowed_book.delete()

        # Update the user's current borrowed books count
        request.user.current_borrowed_books -= 1
        request.user.save()

        return Response({
            "message": f"You have successfully returned '{book.title}'.",
            "fine": fine
        }, status=status.HTTP_200_OK)


#for books related admin functionality


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()
    

class BookAdminViewSet(viewsets.ModelViewSet):
    """
    A viewset for admin users to manage books.
    Provides `create`, `retrieve`, `update`, and `destroy` actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only allow access to authenticated admins

    def create(self, request, *args, **kwargs):
        # Custom behavior for creating a new book
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Custom behavior for updating a book
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Custom behavior for deleting a book
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)