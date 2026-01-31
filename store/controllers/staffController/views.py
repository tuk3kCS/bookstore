"""
Staff Controller - Views for staff-related functionality
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from store.models import (
    Staff, Book, Order, Category, Author, Publisher, 
    Supplier, Inventory, Coupon
)


def staff_required(view_func):
    """Decorator to check if staff is logged in"""
    def wrapper(request, *args, **kwargs):
        staff_id = request.session.get('staff_id')
        if not staff_id:
            messages.error(request, 'Vui lòng đăng nhập để truy cập.')
            return redirect('staff_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_login(request):
    """Staff login"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Vui lòng nhập email và mật khẩu.')
            return render(request, 'staff/login.html', {'email': email})
        
        try:
            staff = Staff.objects.get(email=email, is_active=True)
            if staff.check_password(password):
                # Login successful
                request.session['staff_id'] = staff.id
                request.session['staff_name'] = staff.name
                request.session['staff_role'] = staff.staff_role.code if staff.staff_role else 'staff'
                
                messages.success(request, f'Chào mừng {staff.name}!')
                return redirect('staff_dashboard')
            else:
                messages.error(request, 'Mật khẩu không đúng.')
        except Staff.DoesNotExist:
            messages.error(request, 'Tài khoản không tồn tại hoặc đã bị vô hiệu hóa.')
        
        return render(request, 'staff/login.html', {'email': email})
    
    return render(request, 'staff/login.html')


def staff_logout(request):
    """Staff logout"""
    request.session.pop('staff_id', None)
    request.session.pop('staff_name', None)
    request.session.pop('staff_role', None)
    
    messages.success(request, 'Đăng xuất thành công!')
    return redirect('staff_login')


@staff_required
def staff_dashboard(request):
    """Staff dashboard"""
    # Get statistics
    total_books = Book.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    low_stock_books = Book.objects.filter(stock_quantity__lt=10).count()
    total_categories = Category.objects.count()
    total_authors = Author.objects.count()
    total_publishers = Publisher.objects.count()
    total_suppliers = Supplier.objects.count()
    active_coupons = Coupon.objects.filter(is_active=True).count()
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Low stock books
    low_stock = Book.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')[:5]
    
    # Recent inventory transactions
    recent_inventory = Inventory.objects.select_related('book', 'staff').order_by('-created_at')[:5]
    
    context = {
        'total_books': total_books,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'low_stock_books': low_stock_books,
        'total_categories': total_categories,
        'total_authors': total_authors,
        'total_publishers': total_publishers,
        'total_suppliers': total_suppliers,
        'active_coupons': active_coupons,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
        'recent_inventory': recent_inventory,
    }
    return render(request, 'staff/dashboard.html', context)


@staff_required
def staff_book_list(request):
    """List all books for staff management"""
    books = Book.objects.all().order_by('-created_at')
    
    # Search
    query = request.GET.get('q', '')
    if query:
        books = books.filter(title__icontains=query)
    
    # Pagination
    paginator = Paginator(books, 20)
    page = request.GET.get('page', 1)
    books = paginator.get_page(page)
    
    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'staff/book_list.html', context)


@staff_required
def staff_book_add(request):
    """Add a new book"""
    categories = Category.objects.filter(is_active=True)
    authors = Author.objects.all()
    publishers = Publisher.objects.filter(is_active=True)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author', '')
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '')
        stock_quantity = request.POST.get('stock_quantity', '0')
        category_id = request.POST.get('category', '')
        isbn = request.POST.get('isbn', '').strip()
        publisher_id = request.POST.get('publisher', '')
        publication_year = request.POST.get('publication_year', '')
        image = request.FILES.get('image')
        
        # Validation
        errors = []
        if not title:
            errors.append('Vui lòng nhập tên sách.')
        if not price:
            errors.append('Vui lòng nhập giá sách.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'staff/book_form.html', {
                'title': title,
                'author_id': author_id,
                'description': description,
                'price': price,
                'stock_quantity': stock_quantity,
                'category_id': category_id,
                'isbn': isbn,
                'publisher_id': publisher_id,
                'publication_year': publication_year,
                'categories': categories,
                'authors': authors,
                'publishers': publishers,
            })
        
        # Create book
        book = Book(
            title=title,
            author_id=int(author_id) if author_id else None,
            description=description,
            price=price,
            stock_quantity=int(stock_quantity) if stock_quantity else 0,
            category_id=int(category_id) if category_id else None,
            isbn=isbn if isbn else None,
            publisher_id=int(publisher_id) if publisher_id else None,
            publication_year=int(publication_year) if publication_year else None,
        )
        
        if image:
            book.image = image
        
        book.save()
        messages.success(request, 'Thêm sách thành công!')
        return redirect('staff_book_list')
    
    context = {
        'categories': categories,
        'authors': authors,
        'publishers': publishers,
    }
    return render(request, 'staff/book_form.html', context)


@staff_required
def staff_book_edit(request, book_id):
    """Edit an existing book"""
    book = get_object_or_404(Book, id=book_id)
    categories = Category.objects.filter(is_active=True)
    authors = Author.objects.all()
    publishers = Publisher.objects.filter(is_active=True)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author', '')
        book.author_id = int(author_id) if author_id else None
        book.description = request.POST.get('description', '').strip()
        book.price = request.POST.get('price', book.price)
        book.stock_quantity = int(request.POST.get('stock_quantity', 0))
        category_id = request.POST.get('category', '')
        book.category_id = int(category_id) if category_id else None
        book.isbn = request.POST.get('isbn', '').strip() or None
        publisher_id = request.POST.get('publisher', '')
        book.publisher_id = int(publisher_id) if publisher_id else None
        publication_year = request.POST.get('publication_year', '')
        book.publication_year = int(publication_year) if publication_year else None
        
        if request.FILES.get('image'):
            book.image = request.FILES.get('image')
        
        book.save()
        messages.success(request, 'Cập nhật sách thành công!')
        return redirect('staff_book_list')
    
    context = {
        'book': book,
        'editing': True,
        'categories': categories,
        'authors': authors,
        'publishers': publishers,
    }
    return render(request, 'staff/book_form.html', context)


@staff_required
def staff_book_delete(request, book_id):
    """Delete a book"""
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        messages.success(request, 'Xóa sách thành công!')
    return redirect('staff_book_list')


@staff_required
def staff_order_list(request):
    """List all orders for staff management"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page = request.GET.get('page', 1)
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
        'current_status': status,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'staff/order_list.html', context)


@staff_required
def staff_order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, 'Cập nhật trạng thái đơn hàng thành công!')
            return redirect('staff_order_detail', order_id=order_id)
    
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'staff/order_detail.html', context)
