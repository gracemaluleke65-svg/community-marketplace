from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index, CheckConstraint

db = SQLAlchemy()

class CMP_User(UserMixin, db.Model):
    __tablename__ = 'CMP_users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), nullable=False, default='buyer')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_purchase_made = db.Column(db.Boolean, default=False)
    
    # Relationships
    products = db.relationship('CMP_Product', backref='seller', lazy='dynamic', foreign_keys='CMP_Product.seller_id')
    orders_as_buyer = db.relationship('CMP_Order', backref='buyer', lazy='dynamic', foreign_keys='CMP_Order.buyer_id')
    cart_items = db.relationship('CMP_Cart', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('CMP_Review', backref='user', lazy='dynamic')
    notifications = db.relationship('CMP_Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    favorites = db.relationship('CMP_Favorite', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    used_coupons = db.relationship('CMP_UsedCoupon', backref='user', lazy='dynamic')
    
    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        CheckConstraint("role IN ('buyer', 'seller', 'both', 'admin')", name='valid_role'),
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)
    
    def can_buy(self):
        return self.is_active and self.role in ['buyer', 'both']
    
    def can_sell(self):
        return self.is_active and self.role in ['seller', 'both']
    
    def upgrade_to_seller(self):
        if self.role == 'buyer':
            self.role = 'both'
        elif self.role == 'seller':
            self.role = 'both'
    
    def unread_notifications_count(self):
        return CMP_Notification.query.filter_by(user_id=self.id, is_read=False).count()
    
    def has_used_coupon(self, coupon_id):
        return CMP_UsedCoupon.query.filter_by(user_id=self.id, coupon_id=coupon_id).first() is not None


class CMP_Coupon(db.Model):
    __tablename__ = 'CMP_coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Discount type: percentage, fixed
    discount_type = db.Column(db.String(20), nullable=False, default='percentage')
    discount_value = db.Column(db.Float, nullable=False)  # For percentage: 10 = 10%, for fixed: 50 = R50
    
    # Restrictions
    min_order_amount = db.Column(db.Float, default=0)
    max_discount_amount = db.Column(db.Float, nullable=True)  # Max discount for percentage coupons
    applicable_category = db.Column(db.String(50), nullable=True)
    applicable_seller_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=True)
    
    # Validity
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)
    valid_to = db.Column(db.DateTime, nullable=False)
    
    # Usage limits
    usage_limit = db.Column(db.Integer, nullable=True)  # Total times coupon can be used
    used_count = db.Column(db.Integer, default=0)
    per_user_limit = db.Column(db.Integer, default=1)  # Times per user
    
    # Special flags
    is_active = db.Column(db.Boolean, default=True)
    is_first_purchase_only = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=True)
    
    # Relationships
    seller = db.relationship('CMP_User', foreign_keys=[applicable_seller_id])
    creator = db.relationship('CMP_User', foreign_keys=[created_by])
    used_by = db.relationship('CMP_UsedCoupon', backref='coupon', lazy='dynamic')
    
    __table_args__ = (
        Index('idx_coupon_code_active', 'code', 'is_active'),
        Index('idx_coupon_validity', 'valid_from', 'valid_to'),
        CheckConstraint("discount_type IN ('percentage', 'fixed')", name='valid_discount_type'),
        CheckConstraint('discount_value > 0', name='positive_discount'),
        CheckConstraint('min_order_amount >= 0', name='non_negative_min_order'),
    )
    
    def is_valid_for_user(self, user, cart_total=0):
        """Check if coupon is valid for a specific user"""
        if not self.is_active:
            return False, "This coupon is no longer active"
        
        now = datetime.utcnow()
        if now < self.valid_from:
            return False, f"This coupon is not valid until {self.valid_from.strftime('%Y-%m-%d')}"
        
        if now > self.valid_to:
            return False, "This coupon has expired"
        
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "This coupon has reached its usage limit"
        
        if user and self.per_user_limit:
            user_uses = CMP_UsedCoupon.query.filter_by(user_id=user.id, coupon_id=self.id).count()
            if user_uses >= self.per_user_limit:
                return False, f"You have already used this coupon {self.per_user_limit} time(s)"
        
        if user and self.is_first_purchase_only and user.first_purchase_made:
            return False, "This coupon is only for first-time purchasers"
        
        if cart_total > 0 and self.min_order_amount > 0 and cart_total < self.min_order_amount:
            return False, f"Minimum order of R{self.min_order_amount:.2f} required"
        
        return True, "Valid"
    
    def calculate_discount(self, subtotal):
        """Calculate discount amount based on coupon type"""
        if self.discount_type == 'percentage':
            discount = subtotal * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return round(discount, 2)
        else:  # fixed
            return min(self.discount_value, subtotal)
    
    def mark_used(self, user, order_id):
        """Mark coupon as used by a user"""
        used_coupon = CMP_UsedCoupon(
            user_id=user.id,
            coupon_id=self.id,
            order_id=order_id,
            discount_amount=0  # Will be updated when order is processed
        )
        self.used_count += 1
        db.session.add(used_coupon)
        return used_coupon
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'min_order_amount': self.min_order_amount,
            'valid_to': self.valid_to.strftime('%Y-%m-%d') if self.valid_to else None,
            'is_first_purchase_only': self.is_first_purchase_only,
            'discount_text': f"{self.discount_value}%" if self.discount_type == 'percentage' else f"R{self.discount_value:.2f}"
        }


class CMP_UsedCoupon(db.Model):
    __tablename__ = 'CMP_used_coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('CMP_coupons.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('CMP_orders.id'), nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_used_coupon_user', 'user_id'),
        Index('idx_used_coupon_coupon', 'coupon_id'),
    )


class CMP_Favorite(db.Model):
    __tablename__ = 'CMP_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('CMP_products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('CMP_Product', backref='favorited_by')
    
    __table_args__ = (
        Index('idx_favorite_user_product', 'user_id', 'product_id', unique=True),
        Index('idx_favorite_product', 'product_id'),
    )


class CMP_Notification(db.Model):
    __tablename__ = 'CMP_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), default='info')
    link_url = db.Column(db.String(500), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_notification_user_read', 'user_id', 'is_read'),
        Index('idx_notification_created', 'created_at'),
        CheckConstraint("notification_type IN ('info', 'success', 'warning', 'danger', 'order', 'product', 'system')", name='valid_type'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type,
            'link_url': self.link_url,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'time_ago': self.get_time_ago()
        }
    
    def get_time_ago(self):
        if not self.created_at:
            return "Just now"
        
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 365:
            return f"{diff.days // 365} year{'s' if diff.days // 365 > 1 else ''} ago"
        elif diff.days > 30:
            return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hour{'s' if diff.seconds // 3600 > 1 else ''} ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minute{'s' if diff.seconds // 60 > 1 else ''} ago"
        else:
            return "Just now"


class CMP_Product(db.Model):
    __tablename__ = 'CMP_products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    stock_quantity = db.Column(db.Integer, default=1)
    category = db.Column(db.String(50), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('CMP_OrderItem', backref='product', lazy='dynamic')
    cart_items = db.relationship('CMP_Cart', backref='product', lazy='dynamic')
    reviews = db.relationship('CMP_Review', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_product_approved_active', 'is_approved', 'is_active'),
        Index('idx_product_seller', 'seller_id', 'is_active'),
        CheckConstraint('price > 0', name='positive_price'),
        CheckConstraint('stock_quantity >= 0', name='non_negative_stock'),
    )


class CMP_Cart(db.Model):
    __tablename__ = 'CMP_cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('CMP_products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_cart_user', 'user_id'),
        CheckConstraint('quantity > 0', name='positive_quantity'),
    )


class CMP_Order(db.Model):
    __tablename__ = 'CMP_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    final_amount = db.Column(db.Float, nullable=False)
    coupon_code = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='pending')
    shipping_address = db.Column(db.Text, nullable=False)
    payment_intent_id = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CMP_OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    used_coupons = db.relationship('CMP_UsedCoupon', backref='order', lazy='dynamic')
    
    __table_args__ = (
        Index('idx_order_buyer', 'buyer_id'),
        Index('idx_order_status', 'status'),
        CheckConstraint("status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')", name='valid_status'),
    )


class CMP_OrderItem(db.Model):
    __tablename__ = 'CMP_order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('CMP_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('CMP_products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)
    
    __table_args__ = (
        Index('idx_orderitem_order', 'order_id'),
        CheckConstraint('quantity > 0', name='positive_quantity'),
        CheckConstraint('price_at_time > 0', name='positive_price'),
    )


class CMP_Review(db.Model):
    __tablename__ = 'CMP_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('CMP_products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('CMP_users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_review_product', 'product_id'),
        Index('idx_review_user', 'user_id'),
        CheckConstraint('rating BETWEEN 1 AND 5', name='valid_rating'),
    )