# Bookstore Management System - Project Context

## 1. Giới thiệu dự án

**Tên dự án:** Bookstore Management System  
**Kiến trúc:** Monolithic MVC nâng cao - Domain Package MVC  
**Mục tiêu:** Xây dựng hệ thống quản lý nhà sách trực tuyến với cấu trúc chia package theo miền nghiệp vụ (book, customer, staff, order, inventory) trong tầng Model và Controller.

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python 3 |
| Framework | Django |
| Frontend | HTML, CSS, Bootstrap 5 |
| Database | MySQL |
| ORM | Django ORM |

## 3. Tổng quan Models (20 lớp)

| STT | Domain | Model | Mô tả |
|-----|--------|-------|-------|
| 1 | Book | Book | Thông tin sách |
| 2 | Book | Rating | Đánh giá sách (điểm) |
| 3 | Book | Category | Danh mục sách |
| 4 | Book | Author | Tác giả |
| 5 | Book | Publisher | Nhà xuất bản |
| 6 | Book | Review | Bài đánh giá chi tiết |
| 7 | Customer | Customer | Khách hàng |
| 8 | Customer | Address | Địa chỉ giao hàng |
| 9 | Customer | Wishlist | Danh sách yêu thích |
| 10 | Customer | WishlistItem | Sách trong danh sách yêu thích |
| 11 | Staff | Staff | Nhân viên |
| 12 | Order | Cart | Giỏ hàng |
| 13 | Order | CartItem | Sách trong giỏ hàng |
| 14 | Order | Order | Đơn hàng |
| 15 | Order | OrderItem | Sách trong đơn hàng |
| 16 | Order | Payment | Phương thức thanh toán |
| 17 | Order | Shipping | Phương thức giao hàng |
| 18 | Order | Coupon | Mã giảm giá |
| 19 | Inventory | Supplier | Nhà cung cấp |
| 20 | Inventory | Inventory | Giao dịch nhập/xuất kho |

## 4. Chức năng hệ thống

### 4.1. Quản lý sách (Book Domain)
- Nhân viên nhập sách vào kho
- Khách hàng tìm kiếm và xem sách
- Hiển thị danh sách sách theo danh mục, tác giả, nhà xuất bản
- Xem chi tiết sách
- Đánh giá sách (Rating & Review)

### 4.2. Quản lý khách hàng (Customer Domain)
- Đăng ký tài khoản
- Đăng nhập/Đăng xuất
- Quản lý thông tin cá nhân
- Quản lý địa chỉ giao hàng
- Quản lý danh sách yêu thích (Wishlist)

### 4.3. Quản lý nhân viên (Staff Domain)
- Đăng nhập nhân viên
- Quản lý kho sách (thêm/sửa/xóa sách)
- Quản lý danh mục, tác giả, nhà xuất bản
- Quản lý nhà cung cấp
- Quản lý nhập/xuất kho
- Quản lý mã giảm giá
- Xem danh sách đơn hàng

### 4.4. Quản lý đơn hàng (Order Domain)
- Tạo giỏ hàng và thêm sách
- Áp dụng mã giảm giá
- Đặt hàng
- Chọn phương thức thanh toán (Payment)
- Chọn phương thức giao hàng (Shipping)
- Gợi ý sách dựa trên lịch sử mua và rating (Recommendation)

### 4.5. Quản lý kho (Inventory Domain)
- Quản lý nhà cung cấp
- Nhập kho từ nhà cung cấp
- Theo dõi lịch sử nhập/xuất kho
- Điều chỉnh tồn kho

## 5. Kiến trúc hệ thống

### 5.1. Mô hình MVC

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
│                     Model Layer (20 Models)                  │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐   │
│  │book       │ │customer   │ │staff      │ │order      │   │
│  │package    │ │package    │ │package    │ │package    │   │
│  │           │ │           │ │           │ │           │   │
│  │- Book     │ │- Customer │ │- Staff    │ │- Cart     │   │
│  │- Rating   │ │- Address  │ │           │ │- CartItem │   │
│  │- Category │ │- Wishlist │ │           │ │- Order    │   │
│  │- Author   │ │- Wishlist │ │           │ │- OrderItem│   │
│  │- Publisher│ │  Item     │ │           │ │- Payment  │   │
│  │- Review   │ │           │ │           │ │- Shipping │   │
│  │           │ │           │ │           │ │- Coupon   │   │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘   │
│                                                              │
│  ┌───────────┐                                              │
│  │inventory  │                                              │
│  │package    │                                              │
│  │           │                                              │
│  │- Supplier │                                              │
│  │- Inventory│                                              │
│  └───────────┘                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Database                               │
│                        MySQL                                 │
└─────────────────────────────────────────────────────────────┘
```

### 5.2. Biểu đồ luồng dữ liệu

```
[User/Browser] → [URLs Router] → [Controller] → [Model] → [Database]
                                      ↓
                              [Template/View]
                                      ↓
                              [Response to User]
```

## 6. Cấu trúc thư mục dự án

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
    │   │   ├── rating.py        # Rating model
    │   │   ├── category.py      # Category model
    │   │   ├── author.py        # Author model
    │   │   ├── publisher.py     # Publisher model
    │   │   └── review.py        # Review model
    │   │
    │   ├── customer/
    │   │   ├── __init__.py
    │   │   ├── customer.py      # Customer model
    │   │   ├── address.py       # Address model
    │   │   └── wishlist.py      # Wishlist, WishlistItem models
    │   │
    │   ├── staff/
    │   │   ├── __init__.py
    │   │   └── staff.py         # Staff model
    │   │
    │   ├── order/
    │   │   ├── __init__.py
    │   │   ├── cart.py          # Cart, CartItem models
    │   │   ├── order.py         # Order, OrderItem models
    │   │   ├── payment.py       # Payment model
    │   │   ├── shipping.py      # Shipping model
    │   │   └── coupon.py        # Coupon model
    │   │
    │   └── inventory/
    │       ├── __init__.py
    │       ├── supplier.py      # Supplier model
    │       └── inventory.py     # Inventory model
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

## 7. Thiết kế Domain Model (20 Classes)

### 7.1. Book Domain (6 Models)

#### Book
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| title | CharField(200) | Tên sách |
| author | ForeignKey(Author) | Tác giả |
| description | TextField | Mô tả sách |
| price | DecimalField | Giá sách |
| stock_quantity | IntegerField | Số lượng trong kho |
| image | ImageField | Ảnh bìa sách |
| category | ForeignKey(Category) | Danh mục |
| isbn | CharField(13) | Mã ISBN |
| publisher | ForeignKey(Publisher) | Nhà xuất bản |
| publication_year | IntegerField | Năm xuất bản |
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

#### Category
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(100) | Tên danh mục |
| description | TextField | Mô tả |
| parent | ForeignKey(self) | Danh mục cha |
| is_active | BooleanField | Đang hoạt động |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### Author
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(100) | Tên tác giả |
| biography | TextField | Tiểu sử |
| birth_date | DateField | Ngày sinh |
| nationality | CharField(50) | Quốc tịch |
| image | ImageField | Ảnh tác giả |
| website | URLField | Website |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### Publisher
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(200) | Tên nhà xuất bản |
| description | TextField | Mô tả |
| address | TextField | Địa chỉ |
| phone | CharField(20) | Số điện thoại |
| email | EmailField | Email |
| website | URLField | Website |
| logo | ImageField | Logo |
| founded_year | IntegerField | Năm thành lập |
| is_active | BooleanField | Đang hoạt động |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### Review
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng |
| book | ForeignKey(Book) | Sách |
| title | CharField(200) | Tiêu đề đánh giá |
| content | TextField | Nội dung đánh giá |
| pros | TextField | Ưu điểm |
| cons | TextField | Nhược điểm |
| is_verified_purchase | BooleanField | Mua hàng xác thực |
| helpful_count | IntegerField | Số lượt hữu ích |
| is_approved | BooleanField | Đã duyệt |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

### 7.2. Customer Domain (4 Models)

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
| updated_at | DateTimeField | Ngày cập nhật |

#### Address
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng |
| recipient_name | CharField(100) | Tên người nhận |
| phone | CharField(20) | Số điện thoại |
| province | CharField(100) | Tỉnh/Thành phố |
| district | CharField(100) | Quận/Huyện |
| ward | CharField(100) | Phường/Xã |
| street_address | TextField | Địa chỉ chi tiết |
| is_default | BooleanField | Địa chỉ mặc định |
| address_type | CharField(20) | Loại địa chỉ (home/office/other) |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### Wishlist
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng |
| name | CharField(100) | Tên danh sách |
| is_public | BooleanField | Công khai |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### WishlistItem
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| wishlist | ForeignKey(Wishlist) | Danh sách yêu thích |
| book | ForeignKey(Book) | Sách |
| priority | IntegerField | Độ ưu tiên |
| note | TextField | Ghi chú |
| added_at | DateTimeField | Ngày thêm |

### 7.3. Staff Domain (1 Model)

#### Staff
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(100) | Họ tên |
| email | EmailField | Email (unique) |
| password | CharField(128) | Mật khẩu (hashed) |
| role | CharField(20) | Vai trò (admin/staff) |
| phone | CharField(20) | Số điện thoại |
| is_active | BooleanField | Đang hoạt động |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

### 7.4. Order Domain (7 Models)

#### Cart
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng |
| is_active | BooleanField | Trạng thái giỏ hàng |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### CartItem
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| cart | ForeignKey(Cart) | Giỏ hàng |
| book | ForeignKey(Book) | Sách |
| quantity | IntegerField | Số lượng |
| added_at | DateTimeField | Ngày thêm |

#### Order
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer | ForeignKey(Customer) | Khách hàng |
| shipping | ForeignKey(Shipping) | Phương thức giao hàng |
| payment | ForeignKey(Payment) | Phương thức thanh toán |
| total_price | DecimalField | Tổng tiền |
| shipping_fee | DecimalField | Phí giao hàng |
| status | CharField | Trạng thái đơn hàng |
| shipping_address | TextField | Địa chỉ giao hàng |
| shipping_phone | CharField(20) | Số điện thoại |
| note | TextField | Ghi chú |
| created_at | DateTimeField | Ngày đặt hàng |
| updated_at | DateTimeField | Ngày cập nhật |

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
| estimated_days | IntegerField | Số ngày dự kiến |
| is_active | BooleanField | Đang hoạt động |

#### Payment
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| method_name | CharField(100) | Tên phương thức |
| description | TextField | Mô tả |
| is_active | BooleanField | Đang hoạt động |

#### Coupon
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| code | CharField(50) | Mã giảm giá (unique) |
| description | TextField | Mô tả |
| discount_type | CharField(20) | Loại giảm giá (percentage/fixed) |
| discount_value | DecimalField | Giá trị giảm |
| min_purchase | DecimalField | Giá trị đơn hàng tối thiểu |
| max_discount | DecimalField | Giảm tối đa |
| usage_limit | IntegerField | Số lần sử dụng tối đa |
| used_count | IntegerField | Số lần đã sử dụng |
| start_date | DateTimeField | Ngày bắt đầu |
| end_date | DateTimeField | Ngày kết thúc |
| is_active | BooleanField | Đang hoạt động |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

### 7.5. Inventory Domain (2 Models)

#### Supplier
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(200) | Tên nhà cung cấp (unique) |
| contact_person | CharField(100) | Người liên hệ |
| email | EmailField | Email |
| phone | CharField(20) | Số điện thoại |
| address | TextField | Địa chỉ |
| tax_code | CharField(20) | Mã số thuế |
| bank_account | CharField(50) | Số tài khoản ngân hàng |
| bank_name | CharField(100) | Tên ngân hàng |
| payment_terms | TextField | Điều khoản thanh toán |
| is_active | BooleanField | Đang hoạt động |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

#### Inventory
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| book | ForeignKey(Book) | Sách |
| supplier | ForeignKey(Supplier) | Nhà cung cấp |
| staff | ForeignKey(Staff) | Nhân viên thực hiện |
| transaction_type | CharField(20) | Loại giao dịch (import/export/return/adjustment) |
| quantity | IntegerField | Số lượng |
| unit_price | DecimalField | Đơn giá |
| total_amount | DecimalField | Tổng tiền |
| note | TextField | Ghi chú |
| reference_number | CharField(50) | Số tham chiếu |
| created_at | DateTimeField | Ngày tạo |

## 8. ERD (Entity Relationship Diagram)

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              BOOK DOMAIN                                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐   │
│  │ Category  │       │  Author   │       │ Publisher │       │  Review   │   │
│  ├───────────┤       ├───────────┤       ├───────────┤       ├───────────┤   │
│  │ id (PK)   │       │ id (PK)   │       │ id (PK)   │       │ id (PK)   │   │
│  │ name      │       │ name      │       │ name      │       │ customer  │──┐│
│  │ parent    │──┐    │ biography │       │ address   │       │ book (FK) │─┐││
│  │ is_active │  │    │ nationality│      │ website   │       │ title     │ │││
│  └─────┬─────┘  │    └─────┬─────┘       └─────┬─────┘       │ content   │ │││
│        │        │          │                   │             │ helpful   │ │││
│        │        │          │                   │             └───────────┘ │││
│        │        └──────────┼───────────────────┼──────────────────┐        │││
│        │                   │                   │                  │        │││
│        ▼                   ▼                   ▼                  │        │││
│  ┌─────────────────────────────────────────────────────────────┐ │        │││
│  │                          Book                                │ │        │││
│  ├─────────────────────────────────────────────────────────────┤ │        │││
│  │ id (PK)    │ title      │ description │ price               │ │        │││
│  │ author (FK)│ category(FK)│ publisher(FK)│ stock_qty │ isbn  │◄┼────────┘││
│  └──────────────────────────┬──────────────────────────────────┘ │         ││
│                             │                                    │         ││
│                             ▼                                    │         ││
│                       ┌───────────┐                              │         ││
│                       │  Rating   │                              │         ││
│                       ├───────────┤                              │         ││
│                       │ id (PK)   │                              │         ││
│                       │ customer  │◄─────────────────────────────┼─────────┘│
│                       │ book (FK) │                              │          │
│                       │ score     │                              │          │
│                       │ comment   │                              │          │
│                       └───────────┘                              │          │
└──────────────────────────────────────────────────────────────────┼──────────┘
                                                                   │
┌──────────────────────────────────────────────────────────────────┼──────────┐
│                           CUSTOMER DOMAIN                        │          │
├──────────────────────────────────────────────────────────────────┼──────────┤
│                                                                  │          │
│  ┌───────────┐       ┌───────────┐       ┌───────────────┐      │          │
│  │ Customer  │       │  Address  │       │   Wishlist    │      │          │
│  ├───────────┤       ├───────────┤       ├───────────────┤      │          │
│  │ id (PK)   │◄──────│ customer  │       │ id (PK)       │      │          │
│  │ name      │◄──────┼───────────┼───────│ customer (FK) │      │          │
│  │ email     │       │ province  │       │ name          │      │          │
│  │ password  │       │ district  │       │ is_public     │      │          │
│  │ phone     │       │ ward      │       └───────┬───────┘      │          │
│  │ address   │       │ street    │               │              │          │
│  └─────┬─────┘       │ is_default│               ▼              │          │
│        │             └───────────┘       ┌───────────────┐      │          │
│        │                                 │ WishlistItem  │      │          │
│        │                                 ├───────────────┤      │          │
│        │                                 │ wishlist (FK) │      │          │
│        │                                 │ book (FK)     │──────┼──────────┘
│        │                                 │ priority      │
│        │                                 │ note          │
│        │                                 └───────────────┘
└────────┼────────────────────────────────────────────────────────────────────┘
         │
┌────────┼────────────────────────────────────────────────────────────────────┐
│        │                    ORDER DOMAIN                                     │
├────────┼────────────────────────────────────────────────────────────────────┤
│        │                                                                     │
│        ▼                                                                     │
│  ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐ │
│  │   Cart    │       │ CartItem  │       │   Order   │       │ OrderItem │ │
│  ├───────────┤       ├───────────┤       ├───────────┤       ├───────────┤ │
│  │ id (PK)   │◄──────│ cart (FK) │       │ id (PK)   │◄──────│ order(FK) │ │
│  │ customer  │       │ book (FK) │       │ customer  │       │ book (FK) │ │
│  │ is_active │       │ quantity  │       │ shipping  │       │ quantity  │ │
│  └───────────┘       └───────────┘       │ payment   │       │ price     │ │
│                                          │ total     │       └───────────┘ │
│                                          │ status    │                     │
│                                          └─────┬─────┘                     │
│                                                │                           │
│        ┌───────────────────────────────────────┼───────────────────┐       │
│        │                                       │                   │       │
│        ▼                                       ▼                   ▼       │
│  ┌───────────┐                           ┌───────────┐       ┌───────────┐ │
│  │  Coupon   │                           │ Shipping  │       │  Payment  │ │
│  ├───────────┤                           ├───────────┤       ├───────────┤ │
│  │ id (PK)   │                           │ id (PK)   │       │ id (PK)   │ │
│  │ code      │                           │ method    │       │ method    │ │
│  │ discount  │                           │ fee       │       │ description│ │
│  │ min_purchase│                         │ est_days  │       │ is_active │ │
│  │ start/end │                           │ is_active │       └───────────┘ │
│  └───────────┘                           └───────────┘                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           INVENTORY DOMAIN                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────┐       ┌───────────┐       ┌───────────┐                     │
│  │ Supplier  │       │ Inventory │       │   Staff   │                     │
│  ├───────────┤       ├───────────┤       ├───────────┤                     │
│  │ id (PK)   │◄──────│supplier(FK)│       │ id (PK)   │                     │
│  │ name      │       │ book (FK) │───────│ name      │◄────┐               │
│  │ contact   │       │ staff(FK) │───────│ email     │     │               │
│  │ email     │       │ type      │       │ password  │     │               │
│  │ phone     │       │ quantity  │       │ role      │     │               │
│  │ address   │       │ unit_price│       └───────────┘     │               │
│  │ tax_code  │       │ total     │                         │               │
│  │ bank_info │       │ note      │◄────────────────────────┘               │
│  └───────────┘       └───────────┘                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 9. Recommendation System

### 9.1. Nguyên lý
"Customers who bought this also bought..."

### 9.2. Thuật toán
1. Tìm tất cả CartItem có chứa book_id hiện tại
2. Lấy danh sách cart_id từ các CartItem đó
3. Tìm tất cả sách khác trong các cart đó
4. Ưu tiên sách có rating cao từ khách hàng có hành vi tương tự
5. Trả về top N sách gợi ý (loại trừ sách hiện tại)

### 9.3. Code mẫu
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

## 10. API Endpoints

### 10.1. Book URLs (`/books/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/books/` | Danh sách sách |
| GET | `/books/<id>/` | Chi tiết sách |
| GET | `/books/search/?q=` | Tìm kiếm sách |
| POST | `/books/<id>/rate/` | Đánh giá sách |

### 10.2. Customer URLs (`/customer/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/customer/register/` | Đăng ký |
| GET/POST | `/customer/login/` | Đăng nhập |
| GET | `/customer/logout/` | Đăng xuất |
| GET/POST | `/customer/profile/` | Hồ sơ cá nhân |

### 10.3. Staff URLs (`/staff/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/staff/login/` | Đăng nhập nhân viên |
| GET | `/staff/logout/` | Đăng xuất |
| GET | `/staff/dashboard/` | Dashboard |
| GET/POST | `/staff/books/add/` | Thêm sách |
| GET/POST | `/staff/books/<id>/edit/` | Sửa sách |
| POST | `/staff/books/<id>/delete/` | Xóa sách |
| GET | `/staff/orders/` | Danh sách đơn hàng |

### 10.4. Order URLs (`/order/`)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/order/cart/` | Xem giỏ hàng |
| POST | `/order/cart/add/<book_id>/` | Thêm vào giỏ |
| POST | `/order/cart/update/<item_id>/` | Cập nhật số lượng |
| POST | `/order/cart/remove/<item_id>/` | Xóa khỏi giỏ |
| GET/POST | `/order/checkout/` | Thanh toán |
| GET | `/order/history/` | Lịch sử đơn hàng |
| GET | `/order/<id>/` | Chi tiết đơn hàng |

## 11. Hướng dẫn cài đặt và chạy

### 11.1. Yêu cầu hệ thống
- Python 3.8+
- MySQL Server 8.0+
- pip (Python package manager)

### 11.2. Tạo database MySQL

Mở MySQL và chạy lệnh sau để tạo database:

```sql
CREATE DATABASE bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 11.3. Cấu hình database

Mở file `bookstore/settings.py` và cập nhật thông tin kết nối MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'bookstore',
        'USER': 'root',              # Tên user MySQL của bạn
        'PASSWORD': 'your_password', # Mật khẩu MySQL của bạn
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_pure': True,
        },
    }
}
```

### 11.4. Các lệnh cài đặt

```bash
# Bước 1: Di chuyển vào thư mục project
cd bookstore

# Bước 2: Tạo virtual environment (khuyến nghị)
python -m venv venv

# Bước 3: Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bước 4: Cài đặt dependencies
pip install -r requirements.txt

# Bước 5: Tạo migrations cho app store
python manage.py makemigrations store

# Bước 6: Chạy migrate để tạo các bảng trong database
python manage.py migrate

# Bước 7: Tạo dữ liệu mẫu (shipping, payment methods, categories, authors, publishers, suppliers, coupons, staff account, sample books)
python manage.py seed_data

# Bước 8: Chạy server
python manage.py runserver
```

### 11.5. Tóm tắt lệnh (copy nhanh cho Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations store
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### 11.6. Truy cập

| URL | Mô tả |
|-----|-------|
| http://127.0.0.1:8000 | Website chính |
| http://127.0.0.1:8000/staff/login/ | Đăng nhập nhân viên |
| http://127.0.0.1:8000/admin/ | Django Admin |

### 11.7. Tài khoản mặc định

Sau khi chạy lệnh `python manage.py seed_data`, hệ thống sẽ tạo sẵn:

**Tài khoản Staff:**
- Email: `admin@bookstore.vn`
- Password: `admin123`

**Dữ liệu mẫu:**
- 6 danh mục sách (Văn học, Văn học Việt Nam, Kỹ năng sống, CNTT, Kinh tế, Thiếu nhi)
- 6 tác giả (Dale Carnegie, Paulo Coelho, Rosie Nguyễn, Eric Matthes, Robert C. Martin, Nguyễn Nhật Ánh)
- 6 nhà xuất bản (NXB Tổng hợp TP.HCM, NXB Hội Nhà văn, NXB Trẻ, No Starch Press, Pearson, NXB Kim Đồng)
- 3 nhà cung cấp (FAHASA, Phương Nam, Alpha Books)
- 3 mã giảm giá (WELCOME10, FREESHIP, SALE20)
- 3 phương thức giao hàng (Tiêu chuẩn, Nhanh, Hỏa tốc)
- 4 phương thức thanh toán (COD, Chuyển khoản, Ví điện tử, Thẻ tín dụng)
- 6 sách mẫu

## 12. Requirements

```
Django>=4.2
mysql-connector-python>=8.0.0
Pillow>=9.5.0
```

## 13. Kết luận

Hệ thống Bookstore Management được xây dựng theo kiến trúc **Domain Package MVC** với **20 classes/models**, giúp:
- Tách biệt rõ ràng các miền nghiệp vụ (book, customer, staff, order, inventory)
- Dễ dàng bảo trì và mở rộng
- Tuân thủ nguyên tắc Single Responsibility
- Hỗ trợ đầy đủ các chức năng: 
  - Quản lý sách với danh mục, tác giả, nhà xuất bản
  - Quản lý đơn hàng, thanh toán, giao hàng
  - Hệ thống mã giảm giá
  - Quản lý kho và nhà cung cấp
  - Danh sách yêu thích cho khách hàng
  - Gợi ý sách thông minh
