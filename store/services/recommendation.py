"""
Recommendation Service
Provides book recommendations based on purchase history and ratings
"""
from django.db.models import Avg, Count

from store.models import Book, CartItem, Rating


def recommend_books(book_id, limit=4):
    """
    Recommend books based on "Customers who bought this also bought..."
    
    Algorithm:
    1. Find all CartItems containing the current book
    2. Get list of cart_ids from those CartItems
    3. Find all other books in those carts
    4. Prioritize books with high ratings from similar customers
    5. Return top N recommendations (excluding current book)
    
    Args:
        book_id: ID of the current book
        limit: Maximum number of recommendations to return
    
    Returns:
        QuerySet of recommended Book objects
    """
    try:
        # Find all cart items that contain this book
        related_cart_items = CartItem.objects.filter(book_id=book_id)
        
        # Get the cart IDs
        cart_ids = list(related_cart_items.values_list('cart_id', flat=True))
        
        if not cart_ids:
            # If no cart items found, return top rated books
            return get_top_rated_books(book_id, limit)
        
        # Find all books in those carts (excluding the current book)
        recommended_items = CartItem.objects.filter(
            cart_id__in=cart_ids
        ).exclude(
            book_id=book_id
        ).values('book_id').annotate(
            frequency=Count('book_id')
        ).order_by('-frequency')
        
        # Get the book IDs
        book_ids = [item['book_id'] for item in recommended_items[:limit * 2]]
        
        if not book_ids:
            return get_top_rated_books(book_id, limit)
        
        # Get books with their average ratings
        books = Book.objects.filter(
            id__in=book_ids,
            stock_quantity__gt=0
        ).annotate(
            avg_rating=Avg('ratings__score')
        ).order_by('-avg_rating')[:limit]
        
        # If we don't have enough recommendations, add top rated books
        if books.count() < limit:
            additional = get_top_rated_books(
                book_id, 
                limit - books.count(),
                exclude_ids=list(books.values_list('id', flat=True))
            )
            return list(books) + list(additional)
        
        return books
    
    except Exception as e:
        # Fallback to top rated books if any error occurs
        return get_top_rated_books(book_id, limit)


def get_top_rated_books(exclude_book_id, limit=4, exclude_ids=None):
    """
    Get top rated books as fallback recommendations
    
    Args:
        exclude_book_id: ID of book to exclude
        limit: Maximum number of books to return
        exclude_ids: Additional IDs to exclude
    
    Returns:
        QuerySet of top rated Book objects
    """
    books = Book.objects.filter(stock_quantity__gt=0).exclude(id=exclude_book_id)
    
    if exclude_ids:
        books = books.exclude(id__in=exclude_ids)
    
    books = books.annotate(
        avg_rating=Avg('ratings__score'),
        rating_count=Count('ratings')
    ).order_by('-avg_rating', '-rating_count')[:limit]
    
    return books


def get_personalized_recommendations(customer_id, limit=8):
    """
    Get personalized recommendations for a customer based on their purchase
    history and ratings
    
    Args:
        customer_id: ID of the customer
        limit: Maximum number of recommendations to return
    
    Returns:
        QuerySet of recommended Book objects
    """
    from store.models import Order, OrderItem
    
    # Get books the customer has already purchased
    purchased_book_ids = OrderItem.objects.filter(
        order__customer_id=customer_id
    ).values_list('book_id', flat=True).distinct()
    
    # Get highly rated books by the customer
    highly_rated_books = Rating.objects.filter(
        customer_id=customer_id,
        score__gte=4
    ).values_list('book_id', flat=True)
    
    # Find recommendations for each highly rated book
    recommended_book_ids = set()
    for book_id in highly_rated_books:
        recs = recommend_books(book_id, limit=2)
        for rec in recs:
            if isinstance(rec, Book):
                recommended_book_ids.add(rec.id)
            else:
                recommended_book_ids.add(rec)
    
    # Exclude already purchased books
    recommended_book_ids = recommended_book_ids - set(purchased_book_ids)
    
    if not recommended_book_ids:
        # Fallback: return new arrivals
        return Book.objects.filter(
            stock_quantity__gt=0
        ).exclude(
            id__in=purchased_book_ids
        ).order_by('-created_at')[:limit]
    
    # Get recommended books
    books = Book.objects.filter(
        id__in=recommended_book_ids,
        stock_quantity__gt=0
    ).annotate(
        avg_rating=Avg('ratings__score')
    ).order_by('-avg_rating')[:limit]
    
    return books
