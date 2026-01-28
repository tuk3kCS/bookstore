"""
Book Controller - Views for book-related functionality
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.contrib import messages
from django.core.paginator import Paginator

from store.models import Book, Rating, Customer, Category, Author, Publisher, Review
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
    books = Book.objects.select_related('author', 'category', 'publisher').all()
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)
    
    # Author filter
    author_id = request.GET.get('author')
    if author_id:
        books = books.filter(author_id=author_id)
    
    # Publisher filter
    publisher_id = request.GET.get('publisher')
    if publisher_id:
        books = books.filter(publisher_id=publisher_id)
    
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
    
    # Get filter options from models
    categories = Category.objects.filter(is_active=True)
    authors = Author.objects.all()
    publishers = Publisher.objects.filter(is_active=True)
    
    context = {
        'books': books,
        'categories': categories,
        'authors': authors,
        'publishers': publishers,
        'current_category': category_id,
        'current_author': author_id,
        'current_publisher': publisher_id,
        'current_sort': sort,
    }
    return render(request, 'book/list.html', context)


def book_detail(request, book_id):
    """Display book details"""
    book = get_object_or_404(
        Book.objects.select_related('author', 'category', 'publisher'),
        id=book_id
    )
    
    # Get ratings for this book
    ratings = Rating.objects.filter(book=book).select_related('customer')[:10]
    
    # Get reviews for this book
    reviews = Review.objects.filter(book=book, is_approved=True).select_related('customer')[:5]
    
    # Get recommended books
    recommendations = recommend_books(book_id)
    
    # Get books from same author
    same_author_books = []
    if book.author:
        same_author_books = Book.objects.filter(author=book.author).exclude(id=book_id)[:4]
    
    # Check if current customer has rated this book
    customer_rating = None
    customer_review = None
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer_rating = Rating.objects.filter(
            customer_id=customer_id,
            book=book
        ).first()
        customer_review = Review.objects.filter(
            customer_id=customer_id,
            book=book
        ).first()
    
    context = {
        'book': book,
        'ratings': ratings,
        'reviews': reviews,
        'recommendations': recommendations,
        'same_author_books': same_author_books,
        'customer_rating': customer_rating,
        'customer_review': customer_review,
        'average_rating': book.get_average_rating(),
        'rating_count': book.get_rating_count(),
    }
    return render(request, 'book/detail.html', context)


def book_search(request):
    """Search books by title, author, or description"""
    query = request.GET.get('q', '')
    books = []
    
    if query:
        books = Book.objects.select_related('author', 'category', 'publisher').filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(description__icontains=query) |
            Q(isbn__icontains=query) |
            Q(category__name__icontains=query) |
            Q(publisher__name__icontains=query)
        ).distinct()
    
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
