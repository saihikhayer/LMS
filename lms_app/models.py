from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Book(models.Model):
    STATUS_BOOK = [
        ('available', 'Available'),
        ('rental', 'Rented'),
    ]

    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250, null=True, blank=True)
    photo_book = models.ImageField(upload_to='photos', null=True, blank=True)
    photo_author = models.ImageField(upload_to='photos', null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    total_copies = models.PositiveIntegerField(default=1)  # Total number of copies
    available_copies = models.PositiveIntegerField(default=1)  # Available copies
    status = models.CharField(max_length=50, choices=STATUS_BOOK, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title





class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
    def is_overdue(self):
        if self.return_date is None and timezone.now() > self.due_date:
            return True
        return False
