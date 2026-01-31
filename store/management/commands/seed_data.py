"""
Seed initial data for the bookstore
Creates shipping methods, payment methods, categories, authors, publishers, suppliers, coupons and a sample staff account
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from store.models import (
    Shipping, Payment, Staff, Book, 
    Category, Author, Publisher, Supplier, Coupon,
    StaffRole
)


class Command(BaseCommand):
    help = 'Seed initial data for the bookstore'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial data...\n')

        # Create Categories
        self.stdout.write('\n--- Creating Categories ---')
        categories_data = [
            {'name': 'Văn học', 'description': 'Sách văn học trong nước và nước ngoài'},
            {'name': 'Văn học Việt Nam', 'description': 'Tác phẩm văn học Việt Nam'},
            {'name': 'Kỹ năng sống', 'description': 'Sách phát triển bản thân và kỹ năng sống'},
            {'name': 'Công nghệ thông tin', 'description': 'Sách về lập trình, CNTT'},
            {'name': 'Kinh tế', 'description': 'Sách kinh tế, quản trị kinh doanh'},
            {'name': 'Thiếu nhi', 'description': 'Sách dành cho thiếu nhi'},
        ]
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = cat
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} category: {cat_data["name"]}')

        # Create Authors
        self.stdout.write('\n--- Creating Authors ---')
        authors_data = [
            {'name': 'Dale Carnegie', 'nationality': 'Mỹ', 'biography': 'Tác giả nổi tiếng với các sách về kỹ năng sống và giao tiếp.'},
            {'name': 'Paulo Coelho', 'nationality': 'Brazil', 'biography': 'Nhà văn Brazil nổi tiếng với tiểu thuyết Nhà giả kim.'},
            {'name': 'Rosie Nguyễn', 'nationality': 'Việt Nam', 'biography': 'Tác giả trẻ người Việt với nhiều tác phẩm truyền cảm hứng.'},
            {'name': 'Eric Matthes', 'nationality': 'Mỹ', 'biography': 'Tác giả chuyên về sách lập trình Python.'},
            {'name': 'Robert C. Martin', 'nationality': 'Mỹ', 'biography': 'Còn gọi là Uncle Bob, chuyên gia về Clean Code.'},
            {'name': 'Nguyễn Nhật Ánh', 'nationality': 'Việt Nam', 'biography': 'Nhà văn nổi tiếng với các tác phẩm về tuổi thơ Việt Nam.'},
        ]
        authors = {}
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults=author_data
            )
            authors[author_data['name']] = author
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} author: {author_data["name"]}')

        # Create Publishers
        self.stdout.write('\n--- Creating Publishers ---')
        publishers_data = [
            {'name': 'NXB Tổng hợp TP.HCM', 'address': 'TP. Hồ Chí Minh', 'phone': '028 38225340'},
            {'name': 'NXB Hội Nhà văn', 'address': 'Hà Nội', 'phone': '024 38222135'},
            {'name': 'NXB Trẻ', 'address': 'TP. Hồ Chí Minh', 'phone': '028 39316289'},
            {'name': 'No Starch Press', 'address': 'San Francisco, USA', 'website': 'https://nostarch.com'},
            {'name': 'Pearson', 'address': 'London, UK', 'website': 'https://pearson.com'},
            {'name': 'NXB Kim Đồng', 'address': 'Hà Nội', 'phone': '024 39436010'},
        ]
        publishers = {}
        for pub_data in publishers_data:
            pub, created = Publisher.objects.get_or_create(
                name=pub_data['name'],
                defaults=pub_data
            )
            publishers[pub_data['name']] = pub
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} publisher: {pub_data["name"]}')

        # Create Suppliers
        self.stdout.write('\n--- Creating Suppliers ---')
        suppliers_data = [
            {
                'name': 'Công ty Phát hành Sách TP.HCM (FAHASA)',
                'contact_person': 'Nguyễn Văn A',
                'email': 'contact@fahasa.com',
                'phone': '028 38225796',
                'address': '60-62 Lê Lợi, Q.1, TP.HCM',
            },
            {
                'name': 'Nhà sách Phương Nam',
                'contact_person': 'Trần Thị B',
                'email': 'info@phuongnam.com',
                'phone': '028 38221234',
                'address': '940 Đường 3/2, Q.11, TP.HCM',
            },
            {
                'name': 'Công ty Sách Alpha',
                'contact_person': 'Lê Văn C',
                'email': 'sales@alphabooks.vn',
                'phone': '024 37568888',
                'address': 'Hà Nội',
            },
        ]
        for sup_data in suppliers_data:
            sup, created = Supplier.objects.get_or_create(
                name=sup_data['name'],
                defaults=sup_data
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} supplier: {sup_data["name"]}')

        # Create Coupons
        self.stdout.write('\n--- Creating Coupons ---')
        now = timezone.now()
        coupons_data = [
            {
                'code': 'WELCOME10',
                'description': 'Giảm 10% cho khách hàng mới',
                'discount_type': 'percentage',
                'discount_value': 10,
                'min_purchase': 100000,
                'max_discount': 50000,
                'start_date': now,
                'end_date': now + timedelta(days=365),
            },
            {
                'code': 'FREESHIP',
                'description': 'Miễn phí vận chuyển',
                'discount_type': 'fixed',
                'discount_value': 30000,
                'min_purchase': 200000,
                'start_date': now,
                'end_date': now + timedelta(days=90),
            },
            {
                'code': 'SALE20',
                'description': 'Giảm 20% tất cả sách',
                'discount_type': 'percentage',
                'discount_value': 20,
                'min_purchase': 150000,
                'max_discount': 100000,
                'usage_limit': 100,
                'start_date': now,
                'end_date': now + timedelta(days=30),
            },
        ]
        for coupon_data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} coupon: {coupon_data["code"]}')

        # Create Shipping Methods
        self.stdout.write('\n--- Creating Shipping Methods ---')
        shipping_methods = [
            {
                'method_name': 'Giao hàng tiêu chuẩn',
                'fee': 30000,
                'description': 'Giao hàng trong 3-5 ngày làm việc',
                'estimated_days': 5,
            },
            {
                'method_name': 'Giao hàng nhanh',
                'fee': 50000,
                'description': 'Giao hàng trong 1-2 ngày làm việc',
                'estimated_days': 2,
            },
            {
                'method_name': 'Giao hàng hỏa tốc',
                'fee': 80000,
                'description': 'Giao hàng trong ngày (nội thành)',
                'estimated_days': 1,
            },
        ]

        for sm in shipping_methods:
            obj, created = Shipping.objects.get_or_create(
                method_name=sm['method_name'],
                defaults=sm
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} shipping: {sm["method_name"]}')

        # Create Payment Methods
        self.stdout.write('\n--- Creating Payment Methods ---')
        payment_methods = [
            {
                'method_name': 'Thanh toán khi nhận hàng (COD)',
                'description': 'Thanh toán bằng tiền mặt khi nhận hàng',
            },
            {
                'method_name': 'Chuyển khoản ngân hàng',
                'description': 'Chuyển khoản qua tài khoản ngân hàng',
            },
            {
                'method_name': 'Ví điện tử (MoMo, ZaloPay)',
                'description': 'Thanh toán qua ví điện tử',
            },
            {
                'method_name': 'Thẻ tín dụng/Ghi nợ',
                'description': 'Thanh toán qua thẻ Visa, MasterCard',
            },
        ]

        for pm in payment_methods:
            obj, created = Payment.objects.get_or_create(
                method_name=pm['method_name'],
                defaults=pm
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} payment: {pm["method_name"]}')

        # Create Staff Roles
        self.stdout.write('\n--- Creating Staff Roles ---')
        roles_data = [
            {'name': 'Administrator', 'code': 'admin', 'description': 'Quản trị viên hệ thống'},
            {'name': 'Manager', 'code': 'manager', 'description': 'Quản lý cửa hàng'},
            {'name': 'Sales', 'code': 'sales', 'description': 'Nhân viên bán hàng'},
        ]
        roles = {}
        for role_data in roles_data:
            role, created = StaffRole.objects.get_or_create(
                code=role_data['code'],
                defaults=role_data
            )
            roles[role_data['code']] = role
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} role: {role_data["name"]}')

        # Create sample staff account
        self.stdout.write('\n--- Creating Staff Account ---')
        staff_email = 'admin@bookstore.vn'
        if not Staff.objects.filter(email=staff_email).exists():
            staff = Staff(
                name='Admin',
                email=staff_email,
                staff_role=roles.get('admin'),
                phone='0123456789',
            )
            staff.set_password('admin123')
            staff.save()
            self.stdout.write(f'  Created staff: {staff_email} (password: admin123)')
        else:
            self.stdout.write(f'  Staff exists: {staff_email}')

        # Create sample books with relations
        self.stdout.write('\n--- Creating Sample Books ---')
        sample_books = [
            {
                'title': 'Đắc Nhân Tâm',
                'author': authors.get('Dale Carnegie'),
                'description': 'Đắc nhân tâm là quyển sách nổi tiếng nhất, bán chạy nhất và có tầm ảnh hưởng nhất của mọi thời đại.',
                'price': 86000,
                'stock_quantity': 50,
                'category': categories.get('Kỹ năng sống'),
                'publisher': publishers.get('NXB Tổng hợp TP.HCM'),
            },
            {
                'title': 'Nhà Giả Kim',
                'author': authors.get('Paulo Coelho'),
                'description': 'Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị.',
                'price': 79000,
                'stock_quantity': 30,
                'category': categories.get('Văn học'),
                'publisher': publishers.get('NXB Hội Nhà văn'),
            },
            {
                'title': 'Tuổi Trẻ Đáng Giá Bao Nhiêu',
                'author': authors.get('Rosie Nguyễn'),
                'description': 'Bạn hối tiếc vì không nắm bắt lấy một cơ hội nào đó, chẳng có ai là hoàn hảo cả.',
                'price': 90000,
                'stock_quantity': 25,
                'category': categories.get('Kỹ năng sống'),
                'publisher': publishers.get('NXB Hội Nhà văn'),
            },
            {
                'title': 'Python Crash Course',
                'author': authors.get('Eric Matthes'),
                'description': 'A Hands-On, Project-Based Introduction to Programming.',
                'price': 450000,
                'stock_quantity': 20,
                'category': categories.get('Công nghệ thông tin'),
                'publisher': publishers.get('No Starch Press'),
            },
            {
                'title': 'Clean Code',
                'author': authors.get('Robert C. Martin'),
                'description': 'A Handbook of Agile Software Craftsmanship.',
                'price': 520000,
                'stock_quantity': 15,
                'category': categories.get('Công nghệ thông tin'),
                'publisher': publishers.get('Pearson'),
            },
            {
                'title': 'Tôi Thấy Hoa Vàng Trên Cỏ Xanh',
                'author': authors.get('Nguyễn Nhật Ánh'),
                'description': 'Một câu chuyện đẹp về tuổi thơ, gia đình và tình bạn.',
                'price': 110000,
                'stock_quantity': 40,
                'category': categories.get('Văn học Việt Nam'),
                'publisher': publishers.get('NXB Trẻ'),
            },
        ]

        for book_data in sample_books:
            obj, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status} book: {book_data["title"]}')

        self.stdout.write(self.style.SUCCESS('\n========================================'))
        self.stdout.write(self.style.SUCCESS('Seeding completed!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write('\nStaff login:')
        self.stdout.write('  Email: admin@bookstore.vn')
        self.stdout.write('  Password: admin123')
        self.stdout.write('\nSample coupons:')
        self.stdout.write('  WELCOME10 - 10% off for new customers')
        self.stdout.write('  FREESHIP - Free shipping')
        self.stdout.write('  SALE20 - 20% off all books')
