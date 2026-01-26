# Bookstore Management System - Project Context

## 1. Giới thiệu dự án

**Tên dự án:** Bookstore Management System  
**Kiến trúc:** Monolithic MVC nâng cao - Domain Package MVC  
**Mục tiêu:** Xây dựng hệ thống quản lý nhà sách trực tuyến với cấu trúc chia package theo miền nghiệp vụ (book, customer, staff, order) trong tầng Model và Controller.

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python 3 |
| Framework | Django |
| Frontend | HTML, CSS, Bootstrap 5 |
| Database | MySQL |
| ORM | Django ORM |

## 3. Chức năng hệ thống

### 3.1. Quản lý sách (Book Domain)
- Nhân viên nhập sách vào kho
- Khách hàng tìm kiếm và xem sách
- Hiển thị danh sách sách
- Xem chi tiết sách
- Đánh giá sách (Rating)

### 3.2. Quản lý khách hàng (Customer Domain)
- Đăng ký tài khoản
- Đăng nhập/Đăng xuất
- Quản lý thông tin cá nhân

### 3.3. Quản lý nhân viên (Staff Domain)
- Đăng nhập nhân viên
- Quản lý kho sách (thêm/sửa/xóa sách)
- Xem danh sách đơn hàng

### 3.4. Quản lý đơn hàng (Order Domain)
- Tạo giỏ hàng và thêm sách
- Đặt hàng
- Chọn phương thức thanh toán (Payment)
- Chọn phương thức giao hàng (Shipping)
- Gợi ý sách dựa trên lịch sử mua và rating (Recommendation)

## 4. Kiến trúc hệ thống

### 4.1. Mô hình MVC

```
┌─────────────────────────────────────────────────────────────┐
│                      View Layer                              │
│                    HTML Templates                            │
│    (book/, cart/, customer/, staff/, order/)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Controller Layer                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│  │bookController│ │customerCtrl │ │ staffCtrl   │ │orderCtrl││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Model Layer                              │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐   │
│  │book package│ │customer   │ │staff      │ │order      │   │
│  │           │ │package    │ │package    │ │package    │   │
│  │- Book     │ │- Customer │ │- Staff    │ │- Cart     │   │
│  │- Rating   │ │           │ │           │ │- CartItem │   │
│  │           │ │           │ │           │ │- Order    │   │
│  │           │ │           │ │           │ │- OrderItem│   │
│  │           │ │           │ │           │ │- Payment  │   │
│  │           │ │           │ │           │ │- Shipping │   │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Database                               │
│                        MySQL                                 │
└─────────────────────────────────────────────────────────────┘
```

### 4.2. Biểu đồ luồng dữ liệu

```
[User/Browser] → [URLs Router] → [Controller] → [Model] → [Database]
                                      ↓
                              [Template/View]
                                      ↓
                              [Response to User]
```

## 5. Cấu trúc thư mục dự án

```
bookstore/
├── manage.py
├── requirements.txt
├── PROJECT_CONTEXT.md
│
├── bookstore/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── store/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    │
    ├── models/
    │   ├── __init__.py
    │   ├── book/
    │   │   ├── __init__.py
    │   │   ├── book.py          # Book model
    │   │   └── rating.py        # Rating model
    │   │
    │   ├── customer/
    │   │   ├── __init__.py
    │   │   └── customer.py      # Customer model
    │   │
    │   ├── staff/
    │   │   ├── __init__.py
    │   │   └── staff.py         # Staff model
    │   │
    │   └── order/
    │       ├── __init__.py
    │       ├── cart.py          # Cart, CartItem models
    │       ├── order.py         # Order, OrderItem models
    │       ├── payment.py       # Payment model
    │       └── shipping.py      # Shipping model
    │
    ├── controllers/
    │   ├── __init__.py
    │   ├── bookController/
    │   │   ├── __init__.py
    │   │   └── views.py         # Book-related views
    │   │
    │   ├── customerController/
    │   │   ├── __init__.py
    │   │   └── views.py         # Customer-related views
    │   │
    │   ├── staffController/
    │   │   ├── __init__.py
    │   │   └── views.py         # Staff-related views
    │   │
    │   └── orderController/
    │       ├── __init__.py
    │       └── views.py         # Order, Cart-related views
    │
    ├── services/
    │   ├── __init__.py
    │   └── recommendation.py    # Book recommendation service
    │
    ├── urls/
    │   ├── __init__.py
    │   ├── book_urls.py
    │   ├── customer_urls.py
    │   ├── staff_urls.py
    │   └── order_urls.py
    │
    ├── templates/
    │   ├── base.html
    │   ├── home.html
    │   │
    │   ├── book/
    │   │   ├── list.html
    │   │   ├── detail.html
    │   │   └── search.html
    │   │
    │   ├── customer/
    │   │   ├── login.html
    │   │   ├── register.html
    │   │   └── profile.html
    │   │
    │   ├── staff/
    │   │   ├── login.html
    │   │   ├── dashboard.html
    │   │   ├── book_form.html
    │   │   └── order_list.html
    │   │
    │   ├── cart/
    │   │   └── cart.html
    │   │
    │   └── order/
    │       ├── checkout.html
    │       ├── order_detail.html
    │       └── order_history.html
    │
    └── static/
        ├── css/
        │   └── style.css
        └── js/
            └── main.js
```

## 6. Thiết kế Domain Model

### 6.1. Book Domain

#### Book
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| title | CharField(200) | Tên sách |
| author | CharField(100) | Tên tác giả |
| description | TextField | Mô tả sách |
| price | DecimalField | Giá sách |
| stock_quantity | IntegerField | Số lượng trong kho |
| image | ImageField | Ảnh bìa sách |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### Rating
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng đánh giá |
| book | ForeignKey(Book) | Sách được đánh giá |
| score | IntegerField(1-5) | Điểm đánh giá |
| comment | TextField | Bình luận |
| created_at | DateTimeField | Ngày đánh giá |

### 6.2. Customer Domain

#### Customer
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(100) | Họ tên |
| email | EmailField | Email (unique) |
| password | CharField(128) | Mật khẩu (hashed) |
| phone | CharField(20) | Số điện thoại |
| address | TextField | Địa chỉ |
| created_at | DateTimeField | Ngày đăng ký |

### 6.3. Staff Domain

#### Staff
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(100) | Họ tên |
| email | EmailField | Email (unique) |
| password | CharField(128) | Mật khẩu (hashed) |
| role | CharField(20) | Vai trò (admin/staff) |
| created_at | DateTimeField | Ngày tạo |

### 6.4. Order Domain

#### Cart
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng |
| is_active | BooleanField | Trạng thái giỏ hàng |
| created_at | DateTimeField | Ngày tạo |

#### CartItem
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| cart | ForeignKey(Cart) | Giỏ hàng |
| book | ForeignKey(Book) | Sách |
| quantity | IntegerField | Số lượng |

#### Order
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng |
| shipping | ForeignKey(Shipping) | Phương thức giao hàng |
| payment | ForeignKey(Payment) | Phương thức thanh toán |
| total_price | DecimalField | Tổng tiền |
| status | CharField | Trạng thái đơn hàng |
| created_at | DateTimeField | Ngày đặt hàng |

#### OrderItem
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| order | ForeignKey(Order) | Đơn hàng |
| book | ForeignKey(Book) | Sách |
| quantity | IntegerField | Số lượng |
| price | DecimalField | Giá tại thời điểm mua |

#### Shipping
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| method_name | CharField(100) | Tên phương thức |
| fee | DecimalField | Phí giao hàng |
| description | TextField | Mô tả |

#### Payment
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| method_name | CharField(100) | Tên phương thức |
| description | TextField | Mô tả |

## 7. ERD (Entity Relationship Diagram)

```
┌───────────┐       ┌───────────┐       ┌───────────┐
│  Customer │       │   Book    │       │   Staff   │
├───────────┤       ├───────────┤       ├───────────┤
│ id (PK)   │       │ id (PK)   │       │ id (PK)   │
│ name      │       │ title     │       │ name      │
│ email     │       │ author    │       │ email     │
│ password  │       │ price     │       │ password  │
│ phone     │       │ stock_qty │       │ role      │
│ address   │       │ image     │       └───────────┘
└─────┬─────┘       └─────┬─────┘
      │                   │
      │    ┌──────────────┤
      │    │              │
      ▼    ▼              │
┌───────────┐             │
│  Rating   │             │
├───────────┤             │
│ id (PK)   │             │
│ customer  │───┐         │
│ book (FK) │───┤         │
│ score     │   │         │
│ comment   │   │         │
└───────────┘   │         │
                │         │
      ┌─────────┘         │
      │                   │
      ▼                   │
┌───────────┐             │
│   Cart    │             │
├───────────┤             │
│ id (PK)   │             │
│ customer  │             │
│ is_active │             │
└─────┬─────┘             │
      │                   │
      ▼                   ▼
┌───────────┐       ┌───────────┐
│ CartItem  │       │  Order    │
├───────────┤       ├───────────┤
│ id (PK)   │       │ id (PK)   │
│ cart (FK) │       │ customer  │
│ book (FK) │───────│ shipping  │
│ quantity  │       │ payment   │
└───────────┘       │ total     │
                    │ status    │
                    └─────┬─────┘
                          │
      ┌───────────────────┼───────────────────┐
      │                   │                   │
      ▼                   ▼                   ▼
┌───────────┐       ┌───────────┐       ┌───────────┐
│ OrderItem │       │ Shipping  │       │  Payment  │
├───────────┤       ├───────────┤       ├───────────┤
│ id (PK)   │       │ id (PK)   │       │ id (PK)   │
│ order(FK) │       │ method    │       │ method    │
│ book (FK) │       │ fee       │       │ description│
│ quantity  │       │ description│      └───────────┘
│ price     │       └───────────┘
└───────────┘
```

## 8. Recommendation System

### 8.1. Nguyên lý
"Customers who bought this also bought..."

### 8.2. Thuật toán
1. Tìm tất cả CartItem có chứa book_id hiện tại
2. Lấy danh sách cart_id từ các CartItem đó
3. Tìm tất cả sách khác trong các cart đó
4. Ưu tiên sách có rating cao từ khách hàng có hành vi tương tự
5. Trả về top N sách gợi ý (loại trừ sách hiện tại)

### 8.3. Code mẫu
```python
def recommend_books(book_id, limit=4):
    # Tìm các cart chứa sách này
    related = CartItem.objects.filter(book_id=book_id)
    carts = [c.cart_id for c in related]
    
    # Tìm các sách khác trong những cart đó
    items = CartItem.objects.filter(cart_id__in=carts)
    books = Book.objects.filter(id__in=[i.book_id for i in items])
    
    # Loại trừ sách hiện tại và lấy distinct
    return books.exclude(id=book_id).distinct()[:limit]
```

## 9. API Endpoints

### 9.1. Book URLs (`/books/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/books/` | Danh sách sách |
| GET | `/books/<id>/` | Chi tiết sách |
| GET | `/books/search/?q=` | Tìm kiếm sách |
| POST | `/books/<id>/rate/` | Đánh giá sách |

### 9.2. Customer URLs (`/customer/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/customer/register/` | Đăng ký |
| GET/POST | `/customer/login/` | Đăng nhập |
| GET | `/customer/logout/` | Đăng xuất |
| GET/POST | `/customer/profile/` | Hồ sơ cá nhân |

### 9.3. Staff URLs (`/staff/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/staff/login/` | Đăng nhập nhân viên |
| GET | `/staff/logout/` | Đăng xuất |
| GET | `/staff/dashboard/` | Dashboard |
| GET/POST | `/staff/books/add/` | Thêm sách |
| GET/POST | `/staff/books/<id>/edit/` | Sửa sách |
| POST | `/staff/books/<id>/delete/` | Xóa sách |
| GET | `/staff/orders/` | Danh sách đơn hàng |

### 9.4. Order URLs (`/order/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/order/cart/` | Xem giỏ hàng |
| POST | `/order/cart/add/<book_id>/` | Thêm vào giỏ |
| POST | `/order/cart/update/<item_id>/` | Cập nhật số lượng |
| POST | `/order/cart/remove/<item_id>/` | Xóa khỏi giỏ |
| GET/POST | `/order/checkout/` | Thanh toán |
| GET | `/order/history/` | Lịch sử đơn hàng |
| GET | `/order/<id>/` | Chi tiết đơn hàng |

## 10. Hướng dẫn cài đặt và chạy

### 10.1. Yêu cầu
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### 10.2. Cài đặt

```bash
# Clone/setup project
cd bookstore

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Cấu hình database MySQL trong settings.py
# Tạo database 'bookstore' trong MySQL

# Chạy migrations
python manage.py makemigrations store
python manage.py migrate

# Tạo superuser (optional)
python manage.py createsuperuser

# Chạy server
python manage.py runserver
```

### 10.3. Truy cập
- Website: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## 11. Requirements

```
Django>=4.2
mysql-connector-python>=8.0.0
Pillow>=9.5.0
```

## 12. Kết luận

Hệ thống Bookstore Management được xây dựng theo kiến trúc **Domain Package MVC**, giúp:
- Tách biệt rõ ràng các miền nghiệp vụ (book, customer, staff, order)
- Dễ dàng bảo trì và mở rộng
- Tuân thủ nguyên tắc Single Responsibility
- Hỗ trợ đầy đủ các chức năng: quản lý sách, đơn hàng, thanh toán, giao hàng và gợi ý thông minh
