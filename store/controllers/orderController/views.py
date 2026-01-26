"""
Order Controller - Views for order and cart functionality
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from store.models import (
    Book, Customer, Cart, CartItem, 
    Order, OrderItem, Shipping, Payment
)


def customer_required(view_func):
    """Decorator to check if customer is logged in"""
    def wrapper(request, *args, **kwargs):
        customer_id = request.session.get('customer_id')
        if not customer_id:
            messages.error(request, 'Vui lòng đăng nhập để tiếp tục.')
            return redirect('customer_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_cart(request):
    """Get or create cart for current customer"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    
    customer = Customer.objects.get(id=customer_id)
    cart, created = Cart.objects.get_or_create(
        customer=customer,
        is_active=True
    )
    return cart


def cart_view(request):
    """View shopping cart"""
    cart = get_cart(request)
    
    if not cart:
        # Show empty cart for non-logged in users
        return render(request, 'cart/cart.html', {'cart': None})
    
    cart_items = cart.items.select_related('book').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': cart.get_total(),
    }
    return render(request, 'cart/cart.html', context)


@customer_required
def cart_add(request, book_id):
    """Add a book to cart"""
    book = get_object_or_404(Book, id=book_id)
    
    if not book.is_in_stock():
        messages.error(request, 'Sách này hiện đã hết hàng.')
        return redirect('book_detail', book_id=book_id)
    
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > book.stock_quantity:
        messages.error(request, f'Chỉ còn {book.stock_quantity} sách trong kho.')
        return redirect('book_detail', book_id=book_id)
    
    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': quantity}
    )
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > book.stock_quantity:
            messages.error(request, f'Chỉ còn {book.stock_quantity} sách trong kho.')
            return redirect('book_detail', book_id=book_id)
        cart_item.quantity = new_quantity
        cart_item.save()
    
    messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng.')
    
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
        })
    
    return redirect('cart_view')


@customer_required
def cart_update(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer_id=request.session.get('customer_id'))
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
        elif quantity > cart_item.book.stock_quantity:
            messages.error(request, f'Chỉ còn {cart_item.book.stock_quantity} sách trong kho.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Đã cập nhật số lượng.')
    
    return redirect('cart_view')


@customer_required
def cart_remove(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer_id=request.session.get('customer_id'))
    cart_item.delete()
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('cart_view')


@customer_required
def checkout(request):
    """Checkout process"""
    cart = get_cart(request)
    
    if not cart or not cart.items.exists():
        messages.error(request, 'Giỏ hàng của bạn đang trống.')
        return redirect('cart_view')
    
    customer = Customer.objects.get(id=request.session.get('customer_id'))
    shipping_methods = Shipping.objects.filter(is_active=True)
    payment_methods = Payment.objects.filter(is_active=True)
    
    if request.method == 'POST':
        shipping_id = request.POST.get('shipping_method')
        payment_id = request.POST.get('payment_method')
        shipping_address = request.POST.get('shipping_address', '').strip()
        shipping_phone = request.POST.get('shipping_phone', '').strip()
        note = request.POST.get('note', '').strip()
        
        # Validation
        errors = []
        if not shipping_id:
            errors.append('Vui lòng chọn phương thức giao hàng.')
        if not payment_id:
            errors.append('Vui lòng chọn phương thức thanh toán.')
        if not shipping_address:
            errors.append('Vui lòng nhập địa chỉ giao hàng.')
        if not shipping_phone:
            errors.append('Vui lòng nhập số điện thoại.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'order/checkout.html', {
                'cart': cart,
                'cart_items': cart.items.select_related('book').all(),
                'customer': customer,
                'shipping_methods': shipping_methods,
                'payment_methods': payment_methods,
                'shipping_address': shipping_address,
                'shipping_phone': shipping_phone,
                'note': note,
            })
        
        shipping = get_object_or_404(Shipping, id=shipping_id)
        payment = get_object_or_404(Payment, id=payment_id)
        
        # Check stock availability
        for item in cart.items.all():
            if item.quantity > item.book.stock_quantity:
                messages.error(request, f'Sách "{item.book.title}" chỉ còn {item.book.stock_quantity} trong kho.')
                return redirect('cart_view')
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            shipping=shipping,
            payment=payment,
            shipping_fee=shipping.fee,
            shipping_address=shipping_address,
            shipping_phone=shipping_phone,
            note=note,
        )
        
        # Create order items and update stock
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )
            # Update stock
            item.book.stock_quantity -= item.quantity
            item.book.save()
        
        # Calculate total
        order.calculate_total()
        
        # Clear cart
        cart.clear()
        cart.is_active = False
        cart.save()
        
        messages.success(request, 'Đặt hàng thành công!')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('book').all(),
        'customer': customer,
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods,
        'total': cart.get_total(),
    }
    return render(request, 'order/checkout.html', context)


@customer_required
def order_history(request):
    """View order history"""
    customer_id = request.session.get('customer_id')
    orders = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'order/order_history.html', context)


@customer_required
def order_detail(request, order_id):
    """View order details"""
    customer_id = request.session.get('customer_id')
    order = get_object_or_404(Order, id=order_id, customer_id=customer_id)
    
    context = {
        'order': order,
        'order_items': order.items.select_related('book').all(),
    }
    return render(request, 'order/order_detail.html', context)
