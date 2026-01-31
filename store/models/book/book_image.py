from django.db import models


class BookImage(models.Model):
    """Ảnh sách - lưu trữ nhiều ảnh cho mỗi sách"""
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=500)
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_images'
        ordering = ['display_order']

    def __str__(self):
        return f"Image for {self.book.title}"

    def set_as_primary(self):
        """Đặt ảnh này làm ảnh chính"""
        BookImage.objects.filter(book=self.book).update(is_primary=False)
        self.is_primary = True
        self.save()
