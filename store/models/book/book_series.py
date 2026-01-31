from django.db import models


class BookSeries(models.Model):
    """Bộ sách/Series"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='series')
    total_books = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_series'
        verbose_name_plural = 'Book Series'

    def __str__(self):
        return self.name

    def get_books(self):
        return self.books.all().order_by('series_order')

    def update_total_books(self):
        self.total_books = self.books.count()
        self.save()
