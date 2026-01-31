from django.db import models


class BookTag(models.Model):
    """Tag sách - dùng để phân loại và tìm kiếm"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_tags'
        ordering = ['-usage_count', 'name']

    def __str__(self):
        return self.name

    def increment_usage(self):
        self.usage_count += 1
        self.save()

    def get_books(self):
        return self.books.all()
