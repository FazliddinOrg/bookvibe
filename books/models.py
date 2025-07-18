from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=17)
    cover_picture = models.ImageField(default="default_cover.jpg")
    published_year = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(timezone.now().year)],
        help_text="Year the book was published"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return None
        return round(sum(r.stars_given for r in reviews) / reviews.count(), 2)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='author_pics/', blank=True, null=True, default='default_author.jpg'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_authors')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_books')

    def __str__(self):
        return f"{self.book.title} by {self.author.full_name()}"

    class Meta:
        unique_together = ('book', 'author')
        verbose_name = "Book Author"
        verbose_name_plural = "Book Authors"


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} stars for '{self.book.title}' by {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Book Review"
        verbose_name_plural = "Book Reviews"