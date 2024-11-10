from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class CustomUser(AbstractUser):
    # Define roles as choices
    ADMIN = 'ADMIN'
    MEMBER = 'MEMBER'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    ]

    # Role field to distinguish between Admin and Member
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    # Field to track the current number of books borrowed by the member
    current_borrowed_books = models.PositiveIntegerField(default=0)

    # Limit of books a member can borrow
    BORROW_LIMIT = 5

    def is_admin(self):
        """Return True if the user is an admin."""
        return self.role == self.ADMIN

    def is_member(self):
        """Return True if the user is a member."""
        return self.role == self.MEMBER

    def can_borrow_more_books(self):
        """Check if the member has reached the borrow limit."""
        return self.is_member() and self.current_borrowed_books < self.BORROW_LIMIT

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class BorrowedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)  # Reference as a string
    borrow_date = models.DateField(default=timezone.now)
    return_deadline = models.DateField()

    fine_rate = 5  # Fine rate (BDT per day)

    def calculate_fine(self):
        """Calculate fine for overdue books."""
        if timezone.now().date() > self.return_deadline:
            overdue_days = (timezone.now().date() - self.return_deadline).days
            return overdue_days * self.fine_rate
        return 0

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username}"