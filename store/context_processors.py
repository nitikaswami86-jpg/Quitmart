from .models import Cart


def cart_count(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key, user=None).first() if session_key else None

        if cart:
            return {
                'cart_count': cart.total_items,
                'cart_total': cart.total,
            }
    except Exception:
        pass
    return {'cart_count': 0, 'cart_total': 0}
