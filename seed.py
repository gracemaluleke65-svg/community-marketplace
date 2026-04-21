from app import app, db
from models import CMP_User, CMP_Product, CMP_Coupon, CMP_Review
from datetime import datetime, timedelta
import random

def seed_database():
    with app.app_context():
        # Create super admin
        admin = CMP_User.query.filter_by(email='admin@communitymarket.co.za').first()
        if not admin:
            admin = CMP_User(
                full_name='Super Admin',
                email='admin@communitymarket.co.za',
                phone_number='0112345678',
                address='Admin Office, 123 Main Street, Johannesburg, 2000',
                role='admin',
                is_active=True
            )
            admin.set_password('Admin@123')
            db.session.add(admin)
            print("✓ Super admin created!")
        
        # Create a sample seller
        seller = CMP_User.query.filter_by(email='seller@example.com').first()
        if not seller:
            seller = CMP_User(
                full_name='John Seller',
                email='seller@example.com',
                phone_number='0821234567',
                address='123 Main St, Cape Town, 8001',
                role='seller',
                is_active=True
            )
            seller.set_password('Seller@123')
            db.session.add(seller)
            print("✓ Sample seller created!")
        
        # Create another seller
        seller2 = CMP_User.query.filter_by(email='techseller@example.com').first()
        if not seller2:
            seller2 = CMP_User(
                full_name='Tech Guru',
                email='techseller@example.com',
                phone_number='0845566778',
                address='15 Silicon Ave, Johannesburg, 2196',
                role='seller',
                is_active=True
            )
            seller2.set_password('Tech@123')
            db.session.add(seller2)
            print("✓ Second seller created!")
        
        # Create a sample buyer
        buyer = CMP_User.query.filter_by(email='buyer@example.com').first()
        if not buyer:
            buyer = CMP_User(
                full_name='Jane Buyer',
                email='buyer@example.com',
                phone_number='0837654321',
                address='456 Oak Ave, Durban, 4001',
                role='buyer',
                is_active=True
            )
            buyer.set_password('Buyer@123')
            db.session.add(buyer)
            print("✓ Sample buyer created!")
        
        # Create additional buyers for reviews
        buyers = []
        buyer_names = ['Sarah Johnson', 'Michael Brown', 'Lisa Anderson', 'David Wilson', 'Emma Thompson']
        for i, name in enumerate(buyer_names):
            email = f'reviewer{i+1}@example.com'
            existing = CMP_User.query.filter_by(email=email).first()
            if not existing:
                new_buyer = CMP_User(
                    full_name=name,
                    email=email,
                    phone_number=f'081{i+1:03d}45678',
                    address=f'{i+1} Review St, Cape Town, 8001',
                    role='buyer',
                    is_active=True
                )
                new_buyer.set_password('Review@123')
                db.session.add(new_buyer)
                buyers.append(new_buyer)
                print(f"✓ Reviewer {name} created!")
            else:
                buyers.append(existing)
        
        # Create a sample dual role user (both buyer and seller)
        both_user = CMP_User.query.filter_by(email='both@example.com').first()
        if not both_user:
            both_user = CMP_User(
                full_name='Mike Both',
                email='both@example.com',
                phone_number='0841122334',
                address='789 Pine Rd, Pretoria, 0001',
                role='both',
                is_active=True
            )
            both_user.set_password('Both@123')
            db.session.add(both_user)
            print("✓ Sample dual-role user created!")
        
        db.session.commit()
        
        # Get seller IDs after commit
        seller_id = seller.id
        seller2_id = seller2.id
        buyer_id = buyer.id
        both_id = both_user.id
        
        # Seed products with working image URLs
        products_data = [
            # Fashion Category
            {
                'name': 'Handmade Leather Bag',
                'description': 'Beautiful handmade leather bag crafted by local artisans. Perfect for everyday use. Features multiple compartments and adjustable strap.',
                'price': 850.00,
                'stock_quantity': 10,
                'category': 'clothing',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400&h=300&fit=crop'
            },
            {
                'name': 'Premium Denim Jacket',
                'description': 'Classic denim jacket with modern fit. Made from high-quality cotton. Perfect for all seasons.',
                'price': 650.00,
                'stock_quantity': 20,
                'category': 'clothing',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400&h=300&fit=crop'
            },
            {
                'name': 'Running Shoes',
                'description': 'Lightweight running shoes with superior cushioning. Breathable mesh upper for comfort.',
                'price': 899.00,
                'stock_quantity': 15,
                'category': 'sports',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
            },
            
            # Electronics Category
            {
                'name': 'Wireless Noise Cancelling Headphones',
                'description': 'High-quality wireless headphones with active noise cancellation. 30-hour battery life. Bluetooth 5.0.',
                'price': 1299.00,
                'stock_quantity': 25,
                'category': 'electronics',
                'seller_id': seller2_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop'
            },
            {
                'name': 'Smart Watch Pro',
                'description': 'Fitness tracker and smartwatch with heart rate monitor, GPS, and 7-day battery life.',
                'price': 2499.00,
                'stock_quantity': 12,
                'category': 'electronics',
                'seller_id': seller2_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
            },
            {
                'name': 'Wireless Earbuds',
                'description': 'True wireless earbuds with charging case. Crystal clear sound and deep bass.',
                'price': 499.00,
                'stock_quantity': 30,
                'category': 'electronics',
                'seller_id': seller2_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=300&fit=crop'
            },
            
            # Home & Furniture Category
            {
                'name': 'Handcrafted Ceramic Coffee Mug Set',
                'description': 'Set of 4 beautiful handmade ceramic coffee mugs. Microwave and dishwasher safe.',
                'price': 320.00,
                'stock_quantity': 15,
                'category': 'furniture',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=300&fit=crop'
            },
            {
                'name': 'Modern Floor Lamp',
                'description': 'Elegant floor lamp with adjustable brightness. Perfect for living room or bedroom.',
                'price': 450.00,
                'stock_quantity': 8,
                'category': 'furniture',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop'
            },
            {
                'name': 'Wooden Bookshelf',
                'description': 'Solid wood bookshelf with 5 shelves. Perfect for home office or living room.',
                'price': 1899.00,
                'stock_quantity': 5,
                'category': 'furniture',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=400&h=300&fit=crop'
            },
            
            # Books Category
            {
                'name': 'The Great Gatsby (Hardcover)',
                'description': 'Classic American novel by F. Scott Fitzgerald. Collector\'s edition with gold foil cover.',
                'price': 180.00,
                'stock_quantity': 20,
                'category': 'books',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=300&fit=crop'
            },
            {
                'name': 'Python Programming Guide',
                'description': 'Complete guide to Python programming for beginners and intermediate developers.',
                'price': 450.00,
                'stock_quantity': 18,
                'category': 'books',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=300&fit=crop'
            },
            
            # Sports Category
            {
                'name': 'Yoga Mat Premium',
                'description': 'Non-slip yoga mat with carrying strap. 6mm thickness for extra comfort.',
                'price': 299.00,
                'stock_quantity': 25,
                'category': 'sports',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop'
            },
            {
                'name': 'Dumbbell Set 20kg',
                'description': 'Adjustable dumbbell set perfect for home workouts. Includes storage rack.',
                'price': 1299.00,
                'stock_quantity': 10,
                'category': 'sports',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=400&h=300&fit=crop'
            },
            
            # Decorative Wall Mirror
            {
                'name': 'Decorative Wall Mirror',
                'description': 'Elegant wall mirror with decorative frame. Perfect for living room, bedroom, or hallway.',
                'price': 350.00,
                'stock_quantity': 12,
                'category': 'furniture',
                'seller_id': seller_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=300&fit=crop'
            },
            
            # Bluetooth Speaker
            {
                'name': 'Portable Bluetooth Speaker',
                'description': 'Compact wireless speaker with powerful sound, 12-hour battery life, and waterproof design. Perfect for outdoor and indoor use.',
                'price': 599.00,
                'stock_quantity': 20,
                'category': 'electronics',
                'seller_id': seller2_id,
                'is_approved': True,
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop'
            }
        ]
        
        # Add products if they don't exist
        products_added = 0
        products_list = []
        for product_data in products_data:
            existing = CMP_Product.query.filter_by(name=product_data['name']).first()
            if not existing:
                product = CMP_Product(**product_data)
                db.session.add(product)
                products_list.append(product)
                products_added += 1
            else:
                products_list.append(existing)
        
        db.session.commit()
        
        if products_added > 0:
            print(f"✓ {products_added} sample products created!")
        else:
            print("✓ Products already exist!")
        
        # Seed reviews for each product
        reviews_data = {
            'Handmade Leather Bag': [
                (5, "Absolutely stunning bag! The leather quality is exceptional. It's become my everyday go-to bag. Highly recommend!", buyer_id),
                (4, "Beautiful craftsmanship. A bit pricey but worth every cent. Fits my laptop perfectly.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (5, "Best purchase I've made this year! The leather is soft and the bag is spacious.", buyers[1].id if len(buyers) > 1 else buyer_id),
            ],
            'Premium Denim Jacket': [
                (4, "Great quality denim. Fits perfectly. Love the classic look.", buyer_id),
                (5, "This jacket is amazing! Very comfortable and stylish.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (4, "Good material, true to size. Would buy again.", buyers[2].id if len(buyers) > 2 else buyer_id),
            ],
            'Running Shoes': [
                (5, "Most comfortable running shoes ever! Great cushioning and support.", buyer_id),
                (4, "Good shoes for daily runs. Breathable and lightweight.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (5, "Helped me improve my running time. Very responsive and comfortable.", buyers[1].id if len(buyers) > 1 else buyer_id),
            ],
            'Wireless Noise Cancelling Headphones': [
                (5, "Best headphones I've owned! Noise cancellation is top-notch. Battery life is incredible.", buyer_id),
                (5, "Sound quality is amazing. Worth every penny!", buyers[2].id if len(buyers) > 2 else buyer_id),
                (4, "Great headphones. Comfortable for long listening sessions.", buyers[3].id if len(buyers) > 3 else buyer_id),
            ],
            'Smart Watch Pro': [
                (5, "Love this watch! Tracks everything accurately. Battery lasts a full week.", buyer_id),
                (4, "Great features and sleek design. Heart rate monitor is accurate.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (5, "Best smartwatch for fitness enthusiasts. Highly recommend!", buyers[1].id if len(buyers) > 1 else buyer_id),
            ],
            'Wireless Earbuds': [
                (4, "Good sound quality. Battery life is decent. Connectivity is stable.", buyer_id),
                (5, "Excellent value for money! Sound is crisp and clear.", buyers[2].id if len(buyers) > 2 else buyer_id),
                (4, "Comfortable fit and good noise isolation.", buyers[3].id if len(buyers) > 3 else buyer_id),
            ],
            'Handcrafted Ceramic Coffee Mug Set': [
                (5, "Beautiful mugs! Perfect for my morning coffee. The ceramic feels high quality.", buyer_id),
                (5, "Love these mugs! They look great and are dishwasher safe.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (4, "Nice set. The colors are vibrant. Good value.", buyers[4].id if len(buyers) > 4 else buyer_id),
            ],
            'Modern Floor Lamp': [
                (4, "Elegant design. Provides good lighting. Easy to assemble.", buyer_id),
                (5, "Perfect for my living room! Adjustable brightness is a great feature.", buyers[1].id if len(buyers) > 1 else buyer_id),
                (4, "Good quality lamp. Looks exactly as pictured.", buyers[0].id if len(buyers) > 0 else buyer_id),
            ],
            'Wooden Bookshelf': [
                (5, "Sturdy and beautiful bookshelf. Easy to assemble. Holds all my books perfectly.", buyer_id),
                (4, "Great quality wood. Looks expensive but reasonably priced.", buyers[2].id if len(buyers) > 2 else buyer_id),
                (5, "Love this bookshelf! Perfect for my home office.", buyers[3].id if len(buyers) > 3 else buyer_id),
            ],
            'The Great Gatsby (Hardcover)': [
                (5, "Beautiful collector's edition. A timeless classic. The cover is stunning.", buyer_id),
                (5, "One of my favorite books. This edition is gorgeous.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (4, "Great quality hardcover. Perfect gift for book lovers.", buyers[1].id if len(buyers) > 1 else buyer_id),
            ],
            'Python Programming Guide': [
                (5, "Excellent book for beginners! Very clear explanations and great examples.", buyer_id),
                (5, "Best Python book I've read. Highly recommend for aspiring developers.", buyers[2].id if len(buyers) > 2 else buyer_id),
                (4, "Good content. Covers all essential topics.", buyers[3].id if len(buyers) > 3 else buyer_id),
            ],
            'Yoga Mat Premium': [
                (5, "Perfect thickness and non-slip surface. Great for hot yoga.", buyer_id),
                (4, "Good quality mat. Comfortable and easy to clean.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (5, "Best yoga mat I've used! Highly recommend.", buyers[4].id if len(buyers) > 4 else buyer_id),
            ],
            'Dumbbell Set 20kg': [
                (5, "Great for home workouts! Adjustable and easy to use.", buyer_id),
                (4, "Solid build quality. Good value for money.", buyers[1].id if len(buyers) > 1 else buyer_id),
                (5, "Perfect for my home gym. Highly recommend!", buyers[2].id if len(buyers) > 2 else buyer_id),
            ],
            'Decorative Wall Mirror': [
                (5, "Beautiful mirror! Makes my room look bigger. Great quality.", buyer_id),
                (4, "Elegant design. Well-packaged and arrived safely.", buyers[0].id if len(buyers) > 0 else buyer_id),
                (5, "Love this mirror! Perfect for my bedroom.", buyers[3].id if len(buyers) > 3 else buyer_id),
            ],
            'Portable Bluetooth Speaker': [
                (5, "Amazing sound for such a small speaker! Battery lasts long. Waterproof works great!", buyer_id),
                (5, "Best portable speaker I've owned. Great bass and clarity.", buyers[1].id if len(buyers) > 1 else buyer_id),
                (4, "Good sound quality. Perfect for outdoor use.", buyers[2].id if len(buyers) > 2 else buyer_id),
            ],
        }
        
        # Add reviews
        reviews_added = 0
        for product_name, product_reviews in reviews_data.items():
            product = CMP_Product.query.filter_by(name=product_name).first()
            if product:
                for rating, comment, user_id in product_reviews:
                    # Check if review already exists
                    existing_review = CMP_Review.query.filter_by(
                        product_id=product.id,
                        user_id=user_id
                    ).first()
                    
                    if not existing_review:
                        review = CMP_Review(
                            product_id=product.id,
                            user_id=user_id,
                            rating=rating,
                            comment=comment,
                            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                        )
                        db.session.add(review)
                        reviews_added += 1
        
        db.session.commit()
        
        if reviews_added > 0:
            print(f"✓ {reviews_added} sample reviews created!")
        else:
            print("✓ Reviews already exist!")
        
        # Seed coupons with 2028 expiry dates
        now = datetime.utcnow()
        expiry_2028 = datetime(2028, 12, 31, 23, 59, 59)
        
        coupons_data = [
            # Welcome/First Purchase Coupons
            {
                'code': 'WELCOME15',
                'name': 'Welcome to Community Market!',
                'description': 'Get 15% off your first purchase! Welcome to our community.',
                'discount_type': 'percentage',
                'discount_value': 15.00,
                'min_order_amount': 100.00,
                'max_discount_amount': 500.00,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 100,
                'per_user_limit': 1,
                'is_first_purchase_only': True,
                'is_active': True
            },
            {
                'code': 'FIRSTBUY20',
                'name': 'First Time Buyer Special',
                'description': '20% off your first order! Minimum spend R200.',
                'discount_type': 'percentage',
                'discount_value': 20.00,
                'min_order_amount': 200.00,
                'max_discount_amount': 1000.00,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 200,
                'per_user_limit': 1,
                'is_first_purchase_only': True,
                'is_active': True
            },
            
            # Site-wide Sale Coupons
            {
                'code': 'SPRING20',
                'name': 'Spring Sale Extravaganza',
                'description': '20% off everything! Celebrate spring with amazing deals.',
                'discount_type': 'percentage',
                'discount_value': 20.00,
                'min_order_amount': 150.00,
                'max_discount_amount': 1000.00,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 500,
                'per_user_limit': 1,
                'is_first_purchase_only': False,
                'is_active': True
            },
            {
                'code': 'SUMMER25',
                'name': 'Summer Blowout Sale',
                'description': '25% off site-wide! Limited time offer.',
                'discount_type': 'percentage',
                'discount_value': 25.00,
                'min_order_amount': 300.00,
                'max_discount_amount': 1500.00,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 1000,
                'per_user_limit': 1,
                'is_first_purchase_only': False,
                'is_active': True
            },
            
            # Fixed Amount Discounts
            {
                'code': 'SAVE50',
                'name': 'Save R50 on Orders Over R300',
                'description': 'Get R50 off when you spend R300 or more.',
                'discount_type': 'fixed',
                'discount_value': 50.00,
                'min_order_amount': 300.00,
                'max_discount_amount': None,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 200,
                'per_user_limit': 2,
                'is_first_purchase_only': False,
                'is_active': True
            },
            {
                'code': 'SAVE100',
                'name': 'Big Saver - R100 Off',
                'description': 'Save R100 on orders over R500! Great value deal.',
                'discount_type': 'fixed',
                'discount_value': 100.00,
                'min_order_amount': 500.00,
                'max_discount_amount': None,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 150,
                'per_user_limit': 1,
                'is_first_purchase_only': False,
                'is_active': True
            },
            
            # Category-Specific Coupons
            {
                'code': 'ELECTRO10',
                'name': 'Electronics Sale',
                'description': '10% off all electronics! Upgrade your gadgets today.',
                'discount_type': 'percentage',
                'discount_value': 10.00,
                'min_order_amount': 200.00,
                'max_discount_amount': 500.00,
                'applicable_category': 'electronics',
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 300,
                'per_user_limit': 2,
                'is_first_purchase_only': False,
                'is_active': True
            },
            {
                'code': 'FASHION15',
                'name': 'Fashion Flash Sale',
                'description': '15% off all clothing and fashion items!',
                'discount_type': 'percentage',
                'discount_value': 15.00,
                'min_order_amount': 150.00,
                'max_discount_amount': 400.00,
                'applicable_category': 'clothing',
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 250,
                'per_user_limit': 2,
                'is_first_purchase_only': False,
                'is_active': True
            },
            {
                'code': 'BOOKLOVER10',
                'name': 'Book Lover\'s Discount',
                'description': '10% off all books! Expand your library today.',
                'discount_type': 'percentage',
                'discount_value': 10.00,
                'min_order_amount': 100.00,
                'max_discount_amount': 200.00,
                'applicable_category': 'books',
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 150,
                'per_user_limit': 3,
                'is_first_purchase_only': False,
                'is_active': True
            },
            {
                'code': 'SPORTS20',
                'name': 'Sports Equipment Sale',
                'description': '20% off all sports equipment! Get fit for less.',
                'discount_type': 'percentage',
                'discount_value': 20.00,
                'min_order_amount': 250.00,
                'max_discount_amount': 600.00,
                'applicable_category': 'sports',
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 100,
                'per_user_limit': 1,
                'is_first_purchase_only': False,
                'is_active': True
            },
            
            # Seller-Specific Coupons
            {
                'code': 'TECHDEAL',
                'name': 'Tech Guru Special',
                'description': '15% off all products from Tech Guru store!',
                'discount_type': 'percentage',
                'discount_value': 15.00,
                'min_order_amount': 300.00,
                'max_discount_amount': 800.00,
                'applicable_category': None,
                'applicable_seller_id': seller2_id,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 100,
                'per_user_limit': 2,
                'is_first_purchase_only': False,
                'is_active': True
            },
            {
                'code': 'JOHNSFASHION',
                'name': 'John\'s Fashion Store',
                'description': '10% off everything at John Seller\'s store!',
                'discount_type': 'percentage',
                'discount_value': 10.00,
                'min_order_amount': 150.00,
                'max_discount_amount': 300.00,
                'applicable_category': None,
                'applicable_seller_id': seller_id,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 200,
                'per_user_limit': 3,
                'is_first_purchase_only': False,
                'is_active': True
            },
            
            # Flash Sale (Limited Uses)
            {
                'code': 'FLASH50',
                'name': 'Flash Sale - 50% Off',
                'description': 'Limited time flash sale! First 50 customers get 50% off.',
                'discount_type': 'percentage',
                'discount_value': 50.00,
                'min_order_amount': 200.00,
                'max_discount_amount': 2000.00,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 50,
                'per_user_limit': 1,
                'is_first_purchase_only': False,
                'is_active': True
            },
            {
                'code': 'WEEKEND30',
                'name': 'Weekend Special',
                'description': '30% off this weekend only! Don\'t miss out.',
                'discount_type': 'percentage',
                'discount_value': 30.00,
                'min_order_amount': 250.00,
                'max_discount_amount': 1200.00,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 300,
                'per_user_limit': 1,
                'is_first_purchase_only': False,
                'is_active': True
            },
            
            # Free Shipping (Fixed amount covering shipping)
            {
                'code': 'FREESHIP',
                'name': 'Free Shipping',
                'description': 'Get R100 off (covers shipping costs) on orders over R400.',
                'discount_type': 'fixed',
                'discount_value': 100.00,
                'min_order_amount': 400.00,
                'max_discount_amount': None,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 500,
                'per_user_limit': 2,
                'is_first_purchase_only': False,
                'is_active': True
            },
            
            # Holiday Specials
            {
                'code': 'HOLIDAY25',
                'name': 'Holiday Season Sale',
                'description': '25% off everything! Perfect for holiday shopping.',
                'discount_type': 'percentage',
                'discount_value': 25.00,
                'min_order_amount': 200.00,
                'max_discount_amount': 1000.00,
                'applicable_category': None,
                'applicable_seller_id': None,
                'valid_from': now,
                'valid_to': expiry_2028,
                'usage_limit': 1000,
                'per_user_limit': 2,
                'is_first_purchase_only': False,
                'is_active': True
            }
        ]
        
        # Add coupons if they don't exist
        coupons_added = 0
        for coupon_data in coupons_data:
            existing = CMP_Coupon.query.filter_by(code=coupon_data['code']).first()
            if not existing:
                coupon = CMP_Coupon(**coupon_data)
                db.session.add(coupon)
                coupons_added += 1
        
        db.session.commit()
        
        if coupons_added > 0:
            print(f"✓ {coupons_added} sample coupons created!")
        else:
            print("✓ Coupons already exist!")
        
        print("\n" + "="*50)
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*50)
        print("\nLogin Credentials:")
        print("-"*30)
        print("Admin: admin@communitymarket.co.za / Admin@123")
        print("Seller: seller@example.com / Seller@123 (Sell only)")
        print("Seller 2: techseller@example.com / Tech@123 (Electronics)")
        print("Buyer: buyer@example.com / Buyer@123 (Buy only)")
        print("Both: both@example.com / Both@123 (Can buy AND sell)")
        
        print("\nReviewer Accounts (for testing reviews):")
        for i, reviewer in enumerate(buyers):
            print(f"  Reviewer {i+1}: {reviewer.email} / Review@123")
        
        print("\n" + "="*50)
        print("AVAILABLE COUPONS (Expire: December 31, 2028):")
        print("="*50)
        print("\nWelcome/First Purchase:")
        print("  • WELCOME15 - 15% off first order (min R100)")
        print("  • FIRSTBUY20 - 20% off first order (min R200)")
        
        print("\nSite-wide Sales:")
        print("  • SPRING20 - 20% off everything (min R150)")
        print("  • SUMMER25 - 25% off everything (min R300)")
        print("  • HOLIDAY25 - 25% off holiday special (min R200)")
        
        print("\nFixed Amount:")
        print("  • SAVE50 - R50 off (min R300)")
        print("  • SAVE100 - R100 off (min R500)")
        
        print("\nCategory Specific:")
        print("  • ELECTRO10 - 10% off electronics (min R200)")
        print("  • FASHION15 - 15% off clothing (min R150)")
        print("  • BOOKLOVER10 - 10% off books (min R100)")
        print("  • SPORTS20 - 20% off sports (min R250)")
        
        print("\nSeller Specific:")
        print("  • TECHDEAL - 15% off Tech Guru store (min R300)")
        print("  • JOHNSFASHION - 10% off John's Fashion (min R150)")
        
        print("\nFlash Sales (Limited Uses - 50 uses only):")
        print("  • FLASH50 - 50% off (first 50 customers, min R200)")
        print("  • WEEKEND30 - 30% off (min R250)")
        
        print("\nShipping:")
        print("  • FREESHIP - R100 off for shipping (min R400)")
        print("\n" + "="*50)
        print("NOTE: All coupons are valid until December 31, 2028!")
        print("="*50)

if __name__ == '__main__':
    seed_database()