# books/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
