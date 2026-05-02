from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
import json

from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem,
    UserProfile, Wishlist
)
from .forms import UserRegistrationForm, UserLoginForm, CheckoutForm, UserProfileForm


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:12]
    all_products = Product.objects.filter(is_active=True)[:24]
    cart = get_or_create_cart(request)
    cart_product_ids = list(cart.items.values_list('product_id', flat=True))

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'all_products': all_products,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'default')

    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart = get_or_create_cart(request)
    cart_product_ids = list(cart.items.values_list('product_id', flat=True))

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'cart_product_ids': cart_product_ids,
        'total_products': products.count(),
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    cart = get_or_create_cart(request)
    cart_product_ids = list(cart.items.values_list('product_id', flat=True))
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    cart_item = None
    if product.id in cart_product_ids:
        cart_item = cart.items.get(product=product)

    context = {
        'product': product,
        'related_products': related_products,
        'cart_product_ids': cart_product_ids,
        'in_wishlist': in_wishlist,
        'cart_item': cart_item,
    }
    return render(request, 'store/product_detail.html', context)


def cart_view(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'store/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total),
        })

    messages.success(request, f'"{product.name}" cart mein add ho gaya!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product_name} removed from cart',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total),
            'subtotal': float(cart.subtotal),
            'delivery_fee': float(cart.delivery_fee),
        })

    messages.success(request, f'"{product_name}" cart se remove ho gaya!')
    return redirect('cart')


@require_POST
def update_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'cart_total': float(cart.total),
            'subtotal': float(cart.subtotal),
            'delivery_fee': float(cart.delivery_fee),
            'item_total': float(cart_item.total_price) if quantity > 0 else 0,
        })

    return redirect('cart')


def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart clear ho gaya!')
    return redirect('cart')


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Pehle cart mein kuch add karo!')
        return redirect('products')

    profile = getattr(request.user, 'profile', None)
    initial_data = {}
    if profile:
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'phone': profile.phone,
            'address': profile.address,
            'city': profile.city,
            'pincode': profile.pincode,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                pincode=form.cleaned_data['pincode'],
                payment_method=form.cleaned_data['payment_method'],
                subtotal=cart.subtotal,
                delivery_fee=cart.delivery_fee,
                total=cart.total,
                notes=form.cleaned_data.get('notes', ''),
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
                item.product.stock -= item.quantity
                item.product.save()

            cart.items.all().delete()
            messages.success(request, f'Order #{order.order_number} successfully place ho gaya! 🎉')
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm(initial=initial_data)

    context = {'cart': cart, 'form': form}
    return render(request, 'store/checkout.html', context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
            )
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Account ban gaya! 🎉')
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                messages.success(request, f'Welcome back, {user.username}! 👋')
                return redirect(next_url)
            else:
                messages.error(request, 'Username ya password galat hai!')
    else:
        form = UserLoginForm()

    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logout ho gaye!')
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.save()
            messages.success(request, 'Profile update ho gaya!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    orders = Order.objects.filter(user=request.user)[:5]
    context = {'form': form, 'profile': profile, 'recent_orders': orders}
    return render(request, 'store/profile.html', context)



@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    cart = get_or_create_cart(request)
    cart_product_ids = list(cart.items.values_list('product_id', flat=True))
    return render(request, 'store/wishlist.html', {
        'wishlist_items': wishlist_items,
        'cart_product_ids': cart_product_ids,
    })


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        in_wishlist = False
        msg = 'Wishlist se remove ho gaya'
    else:
        in_wishlist = True
        msg = 'Wishlist mein add ho gaya! ❤️'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'in_wishlist': in_wishlist, 'message': msg})

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', '/'))



def search_api(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query),
            is_active=True
        )[:8]
        results = [{'id': p.id, 'name': p.name, 'price': float(p.price),
                    'slug': p.slug, 'category': p.category.name} for p in products]
    return JsonResponse({'results': results})
