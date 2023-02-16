from.models import CartcartItem,Wishlist

# fuction
def countCartItems(request):
    try:
        cartItems = CartcartItem.objects.filter(user=request.user)
        cartItems_count = cartItems.count()
    except:
        cartItems_count = 0
    return dict(cartItems_count=cartItems_count)

def wishlistItemsCount(request):
    try:
        wishlistItems = Wishlist.objects.filter(user=request.user)
        wishlistItemsCount = wishlistItems.count()
    except:
        wishlistItemsCount = 0
    return dict(wishlistItemsCount=wishlistItemsCount)