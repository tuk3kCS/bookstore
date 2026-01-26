"""
Book Controller - Views for book-related functionality
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.contrib import messages
from django.core.paginator import Paginator

from store.models import Book, Rating, Customer
from store.services.recommendation import recommend_books


def home(request):
    """Home page with featured books"""
    # Get featured books (latest books with good ratings)
    featured_books = Book.objects.filter(stock_quantity__gt=0)[:8]
    
    # Get top rated books
    top_rated = Book.objects.annotate(
        avg_rating=Avg('ratings__score')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:4]
    
    # Get new arrivals
    new_arrivals = Book.objects.order_by('-created_at')[:4]
    
    context = {
        'featured_books': featured_books,
        'top_rated': top_rated,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'home.html', context)


def book_list(request):
    """List all books with pagination and filtering"""
    books = Book.objects.all()
    
    # Category filter
    category = request.GET.get('category')
    if category:
        books = books.filter(category=category)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)
    
    # Sort
    sort = request.GET.get('sort', '-created_at')
    if sort == 'price_asc':
        books = books.order_by('price')
    elif sort == 'price_desc':
        books = books.order_by('-price')
    elif sort == 'name':
        books = books.order_by('title')
    elif sort == 'rating':
        books = books.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')
    else:
        books = books.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(books, 12)
    page = request.GET.get('page', 1)
    books = paginator.get_page(page)
    
    # Get categories for filter
    categories = Book.objects.values_list('category', flat=True).distinct()
    categories = [c for c in categories if c]
    
    context = {
        'books': books,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
    }
    return render(request, 'book/list.html', context)


def book_detail(request, book_id):
    """Display book details"""
    book = get_object_or_404(Book, id=book_id)
    
    # Get ratings for this book
    ratings = Rating.objects.filter(book=book).select_related('customer')[:10]
    
    # Get recommended books
    recommendations = recommend_books(book_id)
    
    # Check if current customer has rated this book
    customer_rating = None
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer_rating = Rating.objects.filter(
            customer_id=customer_id,
            book=book
        ).first()
    
    context = {
        'book': book,
        'ratings': ratings,
        'recommendations': recommendations,
        'customer_rating': customer_rating,
        'average_rating': book.get_average_rating(),
        'rating_count': book.get_rating_count(),
    }
    return render(request, 'book/detail.html', context)


def book_search(request):
    """Search books by title, author, or description"""
    query = request.GET.get('q', '')
    books = []
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(books, 12)
    page = request.GET.get('page', 1)
    books = paginator.get_page(page)
    
    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'book/search.html', context)


def book_rate(request, book_id):
    """Rate a book"""
    if request.method != 'POST':
        return redirect('book_detail', book_id=book_id)
    
    # Check if customer is logged in
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Vui lòng đăng nhập để đánh giá sách.')
        return redirect('customer_login')
    
    book = get_object_or_404(Book, id=book_id)
    customer = get_object_or_404(Customer, id=customer_id)
    
    score = request.POST.get('score')
    comment = request.POST.get('comment', '')
    
    if not score or not score.isdigit() or int(score) < 1 or int(score) > 5:
        messages.error(request, 'Điểm đánh giá không hợp lệ.')
        return redirect('book_detail', book_id=book_id)
    
    # Create or update rating
    rating, created = Rating.objects.update_or_create(
        customer=customer,
        book=book,
        defaults={
            'score': int(score),
            'comment': comment
        }
    )
    
    if created:
        messages.success(request, 'Cảm ơn bạn đã đánh giá sách!')
    else:
        messages.success(request, 'Đánh giá của bạn đã được cập nhật.')
    
    return redirect('book_detail', book_id=book_id)
