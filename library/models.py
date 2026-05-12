from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Author(models.Model):

    name = models.CharField(max_length=255)

    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=255)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="author_books"
    )

    genres = models.ManyToManyField(
        Genre,
        related_name="genre_books"
    )

    isbn = models.CharField(max_length=20, unique=True)

    available_copies = models.PositiveIntegerField(default=1)

    total_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class BorrowRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        RETURNED = "RETURNED", "Returned"

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrow_requests"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="borrow_requests"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    requested_at = models.DateTimeField(auto_now_add=True)

    approved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    returned_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} -> {self.book.title}"


class BookReview(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    book = models.ForeignKey(Book,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"