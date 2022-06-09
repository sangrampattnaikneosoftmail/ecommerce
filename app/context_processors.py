from .models import Category, Cart


def categories(request):
    cartItemCount = 0
    if request.user.is_authenticated:
        cartItemCount = Cart.objects.filter(user=request.user).count()
    return {"categories": Category.objects.all(), "cartItemCount": cartItemCount}
