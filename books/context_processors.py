def cart_count(request):
    cart = request.session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
    return {"cart_count": sum(cart.values())}


def recently_viewed(request):
    """Last 10 book IDs (newest first). Pass actual books in views that need them."""
    ids = request.session.get("recently_viewed")
    if not isinstance(ids, list):
        ids = []
    return {"recently_viewed_ids": ids[-10:][::-1]}
