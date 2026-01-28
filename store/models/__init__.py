# Domain Model Package
# Import all models from domain packages

# Book Domain (6 models)
from store.models.book.book import Book
from store.models.book.rating import Rating
from store.models.book.category import Category
from store.models.book.author import Author
from store.models.book.publisher import Publisher
from store.models.book.review import Review

# Customer Domain (4 models)
from store.models.customer.customer import Customer
from store.models.customer.address import Address
from store.models.customer.wishlist import Wishlist, WishlistItem

# Staff Domain (1 model)
from store.models.staff.staff import Staff

# Order Domain (7 models)
from store.models.order.shipping import Shipping
from store.models.order.payment import Payment
from store.models.order.cart import Cart, CartItem
from store.models.order.order import Order, OrderItem
from store.models.order.coupon import Coupon

# Inventory Domain (2 models)
from store.models.inventory.supplier import Supplier
from store.models.inventory.inventory import Inventory

__all__ = [
    # Book Domain
    'Book',
    'Rating',
    'Category',
    'Author',
    'Publisher',
    'Review',
    # Customer Domain
    'Customer',
    'Address',
    'Wishlist',
    'WishlistItem',
    # Staff Domain
    'Staff',
    # Order Domain
    'Shipping',
    'Payment',
    'Cart',
    'CartItem',
    'Order',
    'OrderItem',
    'Coupon',
    # Inventory Domain
    'Supplier',
    'Inventory',
]
