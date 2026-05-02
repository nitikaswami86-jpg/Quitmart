from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, UserProfile


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding QuickMart data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@quickmart.com', 'admin123')
            self.stdout.write('✅ Admin created: admin / admin123')

        # Create test user
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user('testuser', 'test@quickmart.com', 'test123',
                                            first_name='Rahul', last_name='Sharma')
            UserProfile.objects.create(user=user, phone='9876543210', city='Delhi', pincode='110001')
            self.stdout.write('✅ Test user: testuser / test123')

        # Categories
        categories_data = [
            {'name': 'Fruits & Vegetables', 'slug': 'fruits-vegetables', 'icon': '🥦'},
            {'name': 'Dairy & Eggs', 'slug': 'dairy-eggs', 'icon': '🥛'},
            {'name': 'Bakery', 'slug': 'bakery', 'icon': '🍞'},
            {'name': 'Beverages', 'slug': 'beverages', 'icon': '🥤'},
            {'name': 'Snacks', 'slug': 'snacks', 'icon': '🍿'},
            {'name': 'Personal Care', 'slug': 'personal-care', 'icon': '🧴'},
            {'name': 'Cleaning', 'slug': 'cleaning', 'icon': '🧹'},
            {'name': 'Meat & Fish', 'slug': 'meat-fish', 'icon': '🍗'},
            {'name': 'Frozen Foods', 'slug': 'frozen-foods', 'icon': '🧊'},
            {'name': 'Breakfast', 'slug': 'breakfast', 'icon': '🥣'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, _ = Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
            categories[cat_data['slug']] = cat

        self.stdout.write(f'✅ {len(categories)} categories created')

        # Products
        products_data = [
            # Fruits & Vegetables
            {'name': 'Fresh Tomatoes', 'slug': 'fresh-tomatoes', 'category': 'fruits-vegetables',
             'price': 35, 'original_price': 50, 'unit': '500g', 'stock': 150, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400', 'rating': 4.5},
            {'name': 'Baby Spinach', 'slug': 'baby-spinach', 'category': 'fruits-vegetables',
             'price': 29, 'original_price': 40, 'unit': '200g', 'stock': 80,
             'image_url': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400', 'rating': 4.3},
            {'name': 'Yellow Banana', 'slug': 'yellow-banana', 'category': 'fruits-vegetables',
             'price': 49, 'original_price': 60, 'unit': '6 pcs', 'stock': 200, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400', 'rating': 4.6},
            {'name': 'Red Apple', 'slug': 'red-apple', 'category': 'fruits-vegetables',
             'price': 89, 'original_price': 120, 'unit': '4 pcs (~500g)', 'stock': 100, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400', 'rating': 4.7},
            {'name': 'Orange', 'slug': 'orange', 'category': 'fruits-vegetables',
             'price': 59, 'original_price': 80, 'unit': '4 pcs', 'stock': 120,
             'image_url': 'https://images.unsplash.com/photo-1582979512210-99b6a53386f9?w=400', 'rating': 4.4},
            {'name': 'Onion', 'slug': 'onion', 'category': 'fruits-vegetables',
             'price': 25, 'original_price': 35, 'unit': '500g', 'stock': 300,
             'image_url': 'https://images.unsplash.com/photo-1508747703725-719777637510?w=400', 'rating': 4.2},
            {'name': 'Potato', 'slug': 'potato', 'category': 'fruits-vegetables',
             'price': 30, 'original_price': 40, 'unit': '1kg', 'stock': 250,
             'image_url': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400', 'rating': 4.3},
            {'name': 'Mango', 'slug': 'mango', 'category': 'fruits-vegetables',
             'price': 99, 'original_price': 130, 'unit': '2 pcs (~400g)', 'stock': 80, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1605027990121-cbae9e0c0cdf?w=400', 'rating': 4.8},

            # Dairy & Eggs
            {'name': 'Full Cream Milk', 'slug': 'full-cream-milk', 'category': 'dairy-eggs',
             'price': 68, 'original_price': 72, 'unit': '1 Litre', 'stock': 200, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400', 'rating': 4.5},
            {'name': 'Farm Fresh Eggs', 'slug': 'farm-fresh-eggs', 'category': 'dairy-eggs',
             'price': 89, 'original_price': 99, 'unit': '12 pcs', 'stock': 150,
             'image_url': 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400', 'rating': 4.6},
            {'name': 'Amul Butter', 'slug': 'amul-butter', 'category': 'dairy-eggs',
             'price': 55, 'original_price': 60, 'unit': '100g', 'stock': 100,
             'image_url': 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400', 'rating': 4.7},
            {'name': 'Paneer', 'slug': 'paneer', 'category': 'dairy-eggs',
             'price': 79, 'original_price': 95, 'unit': '200g', 'stock': 80, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400', 'rating': 4.4},
            {'name': 'Curd (Dahi)', 'slug': 'curd-dahi', 'category': 'dairy-eggs',
             'price': 45, 'original_price': 52, 'unit': '400g', 'stock': 120,
             'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400', 'rating': 4.5},

            # Bakery
            {'name': 'Whole Wheat Bread', 'slug': 'whole-wheat-bread', 'category': 'bakery',
             'price': 45, 'original_price': 52, 'unit': '400g', 'stock': 100, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400', 'rating': 4.4},
            {'name': 'Chocolate Muffin', 'slug': 'chocolate-muffin', 'category': 'bakery',
             'price': 59, 'original_price': 75, 'unit': '2 pcs', 'stock': 60,
             'image_url': 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=400', 'rating': 4.6},
            {'name': 'Croissant', 'slug': 'croissant', 'category': 'bakery',
             'price': 49, 'original_price': 65, 'unit': '2 pcs', 'stock': 50,
             'image_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400', 'rating': 4.5},

            # Beverages
            {'name': 'Coca Cola', 'slug': 'coca-cola', 'category': 'beverages',
             'price': 40, 'original_price': 45, 'unit': '750ml', 'stock': 200, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=400', 'rating': 4.5},
            {'name': 'Fresh Orange Juice', 'slug': 'fresh-orange-juice', 'category': 'beverages',
             'price': 99, 'original_price': 120, 'unit': '500ml', 'stock': 80,
             'image_url': 'https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=400', 'rating': 4.7},
            {'name': 'Green Tea', 'slug': 'green-tea', 'category': 'beverages',
             'price': 149, 'original_price': 180, 'unit': '25 bags', 'stock': 100,
             'image_url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400', 'rating': 4.6},
            {'name': 'Tropicana Apple Juice', 'slug': 'tropicana-apple-juice', 'category': 'beverages',
             'price': 89, 'original_price': 105, 'unit': '1 Litre', 'stock': 150,
             'image_url': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400', 'rating': 4.4},

            # Snacks
            {'name': "Lay's Classic Chips", 'slug': 'lays-classic-chips', 'category': 'snacks',
             'price': 30, 'original_price': 35, 'unit': '52g', 'stock': 300, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400', 'rating': 4.3},
            {'name': 'Dark Chocolate Bar', 'slug': 'dark-chocolate-bar', 'category': 'snacks',
             'price': 99, 'original_price': 120, 'unit': '100g', 'stock': 150,
             'image_url': 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400', 'rating': 4.7},
            {'name': 'Mixed Nuts', 'slug': 'mixed-nuts', 'category': 'snacks',
             'price': 199, 'original_price': 249, 'unit': '200g', 'stock': 80,
             'image_url': 'https://images.unsplash.com/photo-1570942872213-1242607a6cec?w=400', 'rating': 4.8},
            {'name': 'Kurkure Masala Munch', 'slug': 'kurkure-masala-munch', 'category': 'snacks',
             'price': 20, 'original_price': 22, 'unit': '90g', 'stock': 400,
             'image_url': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=400', 'rating': 4.2},

            # Breakfast
            {'name': 'Kelloggs Corn Flakes', 'slug': 'kelloggs-corn-flakes', 'category': 'breakfast',
             'price': 195, 'original_price': 240, 'unit': '500g', 'stock': 100, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1521303205328-0b20182cf4f1?w=400', 'rating': 4.4},
            {'name': 'Oats', 'slug': 'oats', 'category': 'breakfast',
             'price': 129, 'original_price': 160, 'unit': '500g', 'stock': 120,
             'image_url': 'https://images.unsplash.com/photo-1584263347416-85a696b4eda7?w=400', 'rating': 4.5},

            # Personal Care
            {'name': 'Dove Body Wash', 'slug': 'dove-body-wash', 'category': 'personal-care',
             'price': 299, 'original_price': 360, 'unit': '250ml', 'stock': 80,
             'image_url': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400', 'rating': 4.6},
            {'name': 'Colgate Toothpaste', 'slug': 'colgate-toothpaste', 'category': 'personal-care',
             'price': 99, 'original_price': 115, 'unit': '200g', 'stock': 200, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1556741533-6e6a62bd8b49?w=400', 'rating': 4.5},

            # Cleaning
            {'name': 'Vim Dishwash Bar', 'slug': 'vim-dishwash-bar', 'category': 'cleaning',
             'price': 35, 'original_price': 42, 'unit': '200g', 'stock': 200,
             'image_url': 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=400', 'rating': 4.3},
            {'name': 'Dettol Handwash', 'slug': 'dettol-handwash', 'category': 'cleaning',
             'price': 89, 'original_price': 99, 'unit': '220ml', 'stock': 150, 'is_featured': True,
             'image_url': 'https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=400', 'rating': 4.5},
        ]

        created_count = 0
        for prod_data in products_data:
            cat_slug = prod_data.pop('category')
            prod_data['category'] = categories[cat_slug]
            prod_data.setdefault('description', f"Fresh and high quality {prod_data['name']}. Delivered in 10 minutes.")
            prod_data.setdefault('delivery_time', '10 mins')
            prod_data.setdefault('is_featured', False)
            prod_data.setdefault('review_count', 50)

            _, created = Product.objects.get_or_create(slug=prod_data['slug'], defaults=prod_data)
            if created:
                created_count += 1

        self.stdout.write(f'✅ {created_count} new products created')
        self.stdout.write(self.style.SUCCESS('🎉 QuickMart data seeding complete!'))
        self.stdout.write('📍 Run: python manage.py runserver')
        self.stdout.write('👤 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)')
        self.stdout.write('🛍️  Site: http://127.0.0.1:8000/')
