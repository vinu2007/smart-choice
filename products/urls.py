from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "products/",
        views.product_list,
        name="product_list"
    ),

    path(
        "compare_menu/",
        views.compare_menu,
        name="compare_menu"
    ),

    path(
        "store-compare/",
        views.store_compare_select,
        name="store_compare_select"
    ),

    path(
        "store-compare/<int:pk>",
        views.store_compare,
        name="store_compare"
    ),

    path(
        "compare/",
        views.compare_products,
        name="compare"
    ),

    path(
        "recommend/",
        views.recommend_product,
        name="recommend_product"
    ),

    path(
        "product/<int:pk>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "signup/",
        views.signup_view,      
    name="signup"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "cart/",
        views.cart_view,
        name="cart"
    ),

    path(
        "cart/add/<int:pk>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/remove/<int:pk>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "cart/update/<int:pk>/<str:action>/",
        views.update_cart_quantity,
        name="update_cart_quantity"
    ),

    path(
        "buy-now/<int:product_id>/",
        views.buy_now,
        name="buy_now"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "place-order/",
        views.place_order,
        name="place_order"
    ),

    path(
        "order-success/",
        views.order_success,
        name="order_success"
    ),

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "order/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "order/<int:order_id>/cancel/",
        views.cancel_order,
        name="cancel_order"
    ),

    path(
        "account/",
        views.account,
        name="account"
    ),

    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),

]