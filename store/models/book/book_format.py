from django.db import models


class BookFormat(models.Model):
    """Định dạng sách - Hardcover, Paperback, Ebook, Audiobook"""
    FORMAT_TYPES = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'Ebook'),
        ('audiobook', 'Audiobook'),
    ]
    
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='formats')
    format_type = models.CharField(max_length=20, choices=FORMAT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=20, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    file_size = models.CharField(max_length=50, blank=True)  # For ebook
    duration = models.CharField(max_length=50, blank=True)  # For audiobook
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'book_formats'
        unique_together = ['book', 'format_type']

    def __str__(self):
        return f"{self.book.title} - {self.get_format_type_display()}"

    def get_price_display(self):
        return f"${self.price}"
