from .models import CartItem


def cart_count(request):

    count = 0

    if request.user.is_authenticated:

        count = sum(
            item.quantity
            for item in CartItem.objects.filter(
                user=request.user
            )
        )

    return {
        "cart_count": count
    }