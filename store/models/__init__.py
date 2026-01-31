# Domain Model Package
# Import all models from domain packages (50 models total)

# Book Domain (12 models)
from store.models.book.book import Book
from store.models.book.rating import Rating
from store.models.book.category import Category
from store.models.book.author import Author
from store.models.book.publisher import Publisher
from store.models.book.review import Review
from store.models.book.book_image import BookImage
from store.models.book.book_format import BookFormat
from store.models.book.book_language import BookLanguage
from store.models.book.book_series import BookSeries
from store.models.book.book_tag import BookTag
from store.models.book.book_discount import BookDiscount

# Customer Domain (9 models)
from store.models.customer.customer import Customer
from store.models.customer.address import Address
from store.models.customer.wishlist import Wishlist, WishlistItem
from store.models.customer.customer_group import CustomerGroup
from store.models.customer.loyalty_point import LoyaltyPoint
from store.models.customer.loyalty_transaction import LoyaltyTransaction
from store.models.customer.gift_card import GiftCard
from store.models.customer.notification import Notification

# Staff Domain (6 models)
from store.models.staff.staff import Staff
from store.models.staff.staff_role import StaffRole
from store.models.staff.staff_permission import StaffPermission, RolePermission
from store.models.staff.staff_schedule import StaffSchedule
from store.models.staff.audit_log import AuditLog

# Order Domain (14 models)
from store.models.order.shipping import Shipping
from store.models.order.payment import Payment
from store.models.order.cart import Cart, CartItem
from store.models.order.order import Order, OrderItem
from store.models.order.coupon import Coupon
from store.models.order.shipping_method import ShippingMethod
from store.models.order.shipping_zone import ShippingZone, ShippingZoneRate
from store.models.order.payment_method import PaymentMethod
from store.models.order.tax import Tax, TaxRate
from store.models.order.return_order import ReturnOrder, ReturnOrderItem

# Inventory Domain (7 models)
from store.models.inventory.supplier import Supplier
from store.models.inventory.inventory import Inventory
from store.models.inventory.warehouse import Warehouse
from store.models.inventory.stock_movement import StockMovement
from store.models.inventory.purchase_order import PurchaseOrder, PurchaseOrderItem
from store.models.inventory.inventory_alert import InventoryAlert

# Marketing Domain (5 models)
from store.models.marketing.promotion import Promotion, PromotionRule
from store.models.marketing.banner import Banner
from store.models.marketing.newsletter import Newsletter, NewsletterSubscriber

__all__ = [
    # Book Domain (12)
    'Book', 'Rating', 'Category', 'Author', 'Publisher', 'Review',
    'BookImage', 'BookFormat', 'BookLanguage', 'BookSeries', 'BookTag', 'BookDiscount',
    # Customer Domain (9)
    'Customer', 'Address', 'Wishlist', 'WishlistItem',
    'CustomerGroup', 'LoyaltyPoint', 'LoyaltyTransaction', 'GiftCard', 'Notification',
    # Staff Domain (6)
    'Staff', 'StaffRole', 'StaffPermission', 'RolePermission', 'StaffSchedule', 'AuditLog',
    # Order Domain (14)
    'Shipping', 'Payment', 'Cart', 'CartItem', 'Order', 'OrderItem', 'Coupon',
    'ShippingMethod', 'ShippingZone', 'ShippingZoneRate', 'PaymentMethod',
    'Tax', 'TaxRate', 'ReturnOrder', 'ReturnOrderItem',
    # Inventory Domain (7)
    'Supplier', 'Inventory', 'Warehouse', 'StockMovement',
    'PurchaseOrder', 'PurchaseOrderItem', 'InventoryAlert',
    # Marketing Domain (5)
    'Promotion', 'PromotionRule', 'Banner', 'Newsletter', 'NewsletterSubscriber',
]
