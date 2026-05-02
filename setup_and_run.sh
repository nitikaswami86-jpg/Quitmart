#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  QuickMart – Auto Setup & Run Script
# ═══════════════════════════════════════════════════════════

echo ""
echo "  ⚡  QuickMart – Grocery Delivery App"
echo "  ====================================="
echo ""

# 1. Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q
echo "✅ Dependencies installed"

# 2. Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations --verbosity=0
python manage.py migrate --verbosity=0
echo "✅ Database ready"

# 3. Seed data
echo "🌱 Loading sample data..."
python manage.py seed_data

# 4. Collect static (optional for dev)
# python manage.py collectstatic --noinput -q

echo ""
echo "═══════════════════════════════════════"
echo "  ✅  QuickMart is ready!"
echo "═══════════════════════════════════════"
echo ""
echo "  🌐 Open: http://127.0.0.1:8000"
echo "  👤 Admin: http://127.0.0.1:8000/admin"
echo "     User: admin | Pass: admin123"
echo "  🧪 Demo: testuser | test123"
echo ""

# 5. Start server
echo "🚀 Starting server..."
python manage.py runserver
