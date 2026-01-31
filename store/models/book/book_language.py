from django.db import models


class BookLanguage(models.Model):
    """Ngôn ngữ sách"""
    code = models.CharField(max_length=10, unique=True)  # vi, en, fr, etc.
    name = models.CharField(max_length=100)
    native_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'book_languages'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_book_count(self):
        return self.books.count()
