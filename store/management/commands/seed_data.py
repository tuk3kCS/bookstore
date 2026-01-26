"""
Seed initial data for the bookstore
Creates shipping methods, payment methods, and a sample staff account
"""
from django.core.management.base import BaseCommand
from store.models import Shipping, Payment, Staff, Book


class Command(BaseCommand):
    help = 'Seed initial data for the bookstore'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial data...\n')

        # Create Shipping Methods
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
            if created:
                self.stdout.write(f'  Created shipping: {sm["method_name"]}')
            else:
                self.stdout.write(f'  Shipping exists: {sm["method_name"]}')

        # Create Payment Methods
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
            if created:
                self.stdout.write(f'  Created payment: {pm["method_name"]}')
            else:
                self.stdout.write(f'  Payment exists: {pm["method_name"]}')

        # Create sample staff account
        staff_email = 'admin@bookstore.vn'
        if not Staff.objects.filter(email=staff_email).exists():
            staff = Staff(
                name='Admin',
                email=staff_email,
                role='admin',
                phone='0123456789',
            )
            staff.set_password('admin123')
            staff.save()
            self.stdout.write(f'  Created staff: {staff_email} (password: admin123)')
        else:
            self.stdout.write(f'  Staff exists: {staff_email}')

        # Create sample books
        sample_books = [
            {
                'title': 'Đắc Nhân Tâm',
                'author': 'Dale Carnegie',
                'description': 'Đắc nhân tâm là quyển sách nổi tiếng nhất, bán chạy nhất và có tầm ảnh hưởng nhất của mọi thời đại.',
                'price': 86000,
                'stock_quantity': 50,
                'category': 'Kỹ năng sống',
                'publisher': 'NXB Tổng hợp TP.HCM',
            },
            {
                'title': 'Nhà Giả Kim',
                'author': 'Paulo Coelho',
                'description': 'Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị.',
                'price': 79000,
                'stock_quantity': 30,
                'category': 'Văn học',
                'publisher': 'NXB Hội Nhà văn',
            },
            {
                'title': 'Tuổi Trẻ Đáng Giá Bao Nhiêu',
                'author': 'Rosie Nguyễn',
                'description': 'Bạn hối tiếc vì không nắm bắt lấy một cơ hội nào đó, chẳng có ai là hoàn hảo cả.',
                'price': 90000,
                'stock_quantity': 25,
                'category': 'Kỹ năng sống',
                'publisher': 'NXB Hội Nhà văn',
            },
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'description': 'A Hands-On, Project-Based Introduction to Programming.',
                'price': 450000,
                'stock_quantity': 20,
                'category': 'Công nghệ thông tin',
                'publisher': 'No Starch Press',
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'description': 'A Handbook of Agile Software Craftsmanship.',
                'price': 520000,
                'stock_quantity': 15,
                'category': 'Công nghệ thông tin',
                'publisher': 'Pearson',
            },
            {
                'title': 'Tôi Thấy Hoa Vàng Trên Cỏ Xanh',
                'author': 'Nguyễn Nhật Ánh',
                'description': 'Một câu chuyện đẹp về tuổi thơ, gia đình và tình bạn.',
                'price': 110000,
                'stock_quantity': 40,
                'category': 'Văn học Việt Nam',
                'publisher': 'NXB Trẻ',
            },
        ]

        for book_data in sample_books:
            obj, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'  Created book: {book_data["title"]}')
            else:
                self.stdout.write(f'  Book exists: {book_data["title"]}')

        self.stdout.write(self.style.SUCCESS('\nSeeding completed!'))
        self.stdout.write('\nStaff login:')
        self.stdout.write('  Email: admin@bookstore.vn')
        self.stdout.write('  Password: admin123')
