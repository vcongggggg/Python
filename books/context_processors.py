"""Context processor to inject cart_count and other global data into all templates."""


def cart_context(request):
    cart = request.session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
    return {"cart_count": sum(cart.values()) if cart else 0}
