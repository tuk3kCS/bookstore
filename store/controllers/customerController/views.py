"""
Customer Controller - Views for customer-related functionality
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from store.models import Customer, Order


def customer_register(request):
    """Customer registration"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        
        # Validation
        errors = []
        if not name:
            errors.append('Vui lòng nhập họ tên.')
        if not email:
            errors.append('Vui lòng nhập email.')
        if not password:
            errors.append('Vui lòng nhập mật khẩu.')
        if password != confirm_password:
            errors.append('Mật khẩu xác nhận không khớp.')
        if len(password) < 6:
            errors.append('Mật khẩu phải có ít nhất 6 ký tự.')
        
        # Check if email already exists
        if Customer.objects.filter(email=email).exists():
            errors.append('Email này đã được sử dụng.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'customer/register.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'address': address,
            })
        
        # Create customer
        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
        )
        customer.set_password(password)
        customer.save()
        
        messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect('customer_login')
    
    return render(request, 'customer/register.html')


def customer_login(request):
    """Customer login"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Vui lòng nhập email và mật khẩu.')
            return render(request, 'customer/login.html', {'email': email})
        
        try:
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                # Login successful
                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.name
                request.session['customer_email'] = customer.email
                
                messages.success(request, f'Chào mừng {customer.name}!')
                
                # Redirect to next page or home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Mật khẩu không đúng.')
        except Customer.DoesNotExist:
            messages.error(request, 'Email không tồn tại trong hệ thống.')
        
        return render(request, 'customer/login.html', {'email': email})
    
    return render(request, 'customer/login.html')


def customer_logout(request):
    """Customer logout"""
    # Clear customer session
    request.session.pop('customer_id', None)
    request.session.pop('customer_name', None)
    request.session.pop('customer_email', None)
    
    messages.success(request, 'Đăng xuất thành công!')
    return redirect('home')


def customer_profile(request):
    """Customer profile view and update"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Vui lòng đăng nhập để xem hồ sơ.')
        return redirect('customer_login')
    
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        
        # Update basic info
        if name:
            customer.name = name
            request.session['customer_name'] = name
        if phone:
            customer.phone = phone
        if address:
            customer.address = address
        
        # Update password if provided
        if current_password and new_password:
            if customer.check_password(current_password):
                if len(new_password) >= 6:
                    customer.set_password(new_password)
                    messages.success(request, 'Mật khẩu đã được cập nhật.')
                else:
                    messages.error(request, 'Mật khẩu mới phải có ít nhất 6 ký tự.')
            else:
                messages.error(request, 'Mật khẩu hiện tại không đúng.')
        
        customer.save()
        messages.success(request, 'Thông tin đã được cập nhật.')
        return redirect('customer_profile')
    
    # Get customer's order history
    orders = Order.objects.filter(customer=customer).order_by('-created_at')[:5]
    
    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'customer/profile.html', context)
