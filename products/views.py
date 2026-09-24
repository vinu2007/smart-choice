from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, ProductOffer, CartItem, Order, OrderItem
from urllib.parse import quote
from decimal import Decimal
import re
import requests

from .models import Product


def build_store_options(product):
    """Return the three buying choices shown throughout the storefront."""
    offers = ProductOffer.objects.filter(product=product)
    amazon = offers.filter(store__icontains="amazon").first()
    flipkart = offers.filter(store__icontains="flipkart").first()
    search_term = quote(f"{product.brand} {product.name}")
    money = Decimal("0.01")

    options = [
        {
            "key": "smartchoice",
            "store": "Smart Choice",
            "price": product.price,
            "rating": product.rating,
            "delivery": "Fast delivery from Smart Choice",
            "offer": "Direct checkout and order tracking",
            "url": f"/buy-now/{product.id}/",
            "internal": True,
        },
        {
            "key": "amazon",
            "store": "Amazon",
            "price": amazon.price if amazon else (product.price * Decimal("1.02")).quantize(money),
            "rating": amazon.rating if amazon else None,
            "delivery": amazon.delivery if amazon else "Check delivery on Amazon",
            "offer": amazon.offer if amazon else "Marketplace price",
            "url": amazon.product_url if amazon and amazon.product_url else f"https://www.amazon.in/s?k={search_term}",
            "internal": False,
        },
        {
            "key": "flipkart",
            "store": "Flipkart",
            "price": flipkart.price if flipkart else (product.price * Decimal("0.98")).quantize(money),
            "rating": flipkart.rating if flipkart else None,
            "delivery": flipkart.delivery if flipkart else "Check delivery on Flipkart",
            "offer": flipkart.offer if flipkart else "Marketplace price",
            "url": flipkart.product_url if flipkart and flipkart.product_url else f"https://www.flipkart.com/search?q={search_term}",
            "internal": False,
        },
    ]
    best_option = min(options, key=lambda option: option["price"])
    saving = max(option["price"] for option in options) - best_option["price"]
    return options, best_option, saving

def home(request):

    products = Product.objects.filter(
        is_active=True
    ).order_by("-rating")[:8]

    return render(
        request,
        "home.html",
        {
            "products": products
        }
    )

def account(request):

    return render(
        request,
        "products/account.html"
    )

@login_required(login_url="/login/")
def edit_profile(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        # Username already used by another user
        if User.objects.filter(
            username=username
        ).exclude(
            id=request.user.id
        ).exists():

            return render(
                request,
                "products/edit_profile.html",
                {
                    "error": "Username already exists.",
                    "username": username,
                    "email": email,
                }
            )

        request.user.username = username
        request.user.email = email

        request.user.save()

        return redirect("account")

    return render(
        request,
        "products/edit_profile.html",
        {
            "username": request.user.username,
            "email": request.user.email,
        }
    )

@login_required(login_url="/login/")
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    total = float(product.price)

    context = {
            "buy_now_product": product,
            "buy_now_quantity": 1,
            "buy_now_total": total,
    }

    return render(
        request,
        "products/checkout.html",
        context
    )
def product_list(request):

    products = Product.objects.filter(
        is_active=True
    )

    # Search
    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search)
        )

    # Category
    category = request.GET.get(
        "category",
        ""
    ).strip()

    if category:
        products = products.filter(
            category__iexact=category
        )

    # Brand
    brand = request.GET.get(
        "brand",
        ""
    ).strip()

    if brand:
        products = products.filter(
            brand__iexact=brand
        )

    # Maximum Price
    max_price = request.GET.get(
        "max_price",
        ""
    ).strip()

    if max_price:
        try:
            products = products.filter(
                price__lte=float(max_price)
            )
        except ValueError:
            pass

    # RAM
    ram = request.GET.get(
        "ram",
        ""
    ).strip()

    if ram:
        products = products.filter(
            ram__icontains=ram
        )

    # Storage
    storage = request.GET.get(
        "storage",
        ""
    ).strip()

    if storage:
        products = products.filter(
            storage__icontains=storage
        )

    # Minimum Rating
    min_rating = request.GET.get(
        "min_rating",
        ""
    ).strip()

    if min_rating:
        try:
            products = products.filter(
                rating__gte=float(min_rating)
            )
        except ValueError:
            pass

    # Brands
    brands = Product.objects.filter(
        is_active=True
    ).values_list(
        "brand",
        flat=True
    ).distinct().order_by("brand")

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "brands": brands,
            "search": search,
            "category": category,
            "brand": brand,
            "max_price": max_price,
            "ram": ram,
            "storage": storage,
            "min_rating": min_rating,
        }
    )

    
def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True
    )

    store_options, best_option, you_save = build_store_options(product)

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "store_options": store_options,
            "best_option": best_option,
            "you_save": you_save,
        }
    )

def compare_products(request):

    product_ids = request.GET.getlist("products")

    # Maximum 3 products
    product_ids = product_ids[:3]

    products = Product.objects.filter(
        id__in=product_ids,
        is_active=True
    )

    # Product comparisons are valid only within one category.
    selected_categories = list(products.values_list("category", flat=True).distinct())
    category_mismatch = len(selected_categories) > 1
    if category_mismatch:
        products = Product.objects.none()

    best_product_id = None

    if products.exists():
        best_product = max(
            products,
            key=lambda product: 
    float (product.rating or 0)
        )

        best_product_id = best_product.id
        
    best_product_rating = None

    if products.exists():
        best_product_rating = max(
            float(product.rating or 0)
            for product in products
        )

    best_price = None
    best_ram = None
    best_storage = None

    if products.exists():

        ram_values = []

        storage_values = []

        for product in products:

            if product.ram:
                ram_match = re.search(
                    r"(\d+)",
                    str(product.ram)
                )

                if ram_match:
                    ram_values.append(
                        int(ram_match.group(1))
                    )


            if product.storage:
                storage_match = re.search(
                    r"(\d+)",
                    str(product.storage)
                )

                if storage_match:
                    storage_values.append(
    int(storage_match.group(1))
                )


        if ram_values:
            best_ram = max(ram_values)


        if storage_values:
            best_storage = max(storage_values)
            

    if products.exists():
        best_price = min(
            float(product.price or 0)
            for product in products
        )


    return render(
        request,
        "products/compare.html",
        {
            "products": products,
            "best_product_id": best_product_id,
            "best_product_rating": best_product_rating,
            "best_price": best_price,
            "best_ram": best_ram,
            "best_storage": best_storage,
            "category_mismatch": category_mismatch,
            "available_products": Product.objects.filter(
                is_active=True
            ).order_by("category", "brand", "name"),
        }
    )


def ask_ollama(user_query):

    prompt = f"""
You are Smart Choice AI, a helpful product recommendation assistant.

User question:
"{user_query}"

Your job:

1. Understand what the user is asking.
2. If the user wants a mobile or laptop recommendation, extract:
   CATEGORY: mobile or laptop or none
   BUDGET: number or none
   USAGE: short description or none
   RAM: number or none
   BRAND: brand name or none

3. If the user asks a general technology question, answer it normally.

4. If the question is about products, recommendations, specifications,
   price, RAM, storage, brands, gaming, studying, coding, or performance,
   provide a useful answer.

Return the result in this format:

TYPE: recommendation or general
CATEGORY: mobile or laptop or none
BUDGET: number or none
USAGE: short description or none
RAM: number or none
BRAND: brand name or none
ANSWER: short helpful answer

Do not invent product specifications.
"""

    try:

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",

            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },

            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        ).strip()

    except requests.RequestException as e:

        print("OLLAMA ERROR:", e)

        return ""

def generate_ai_explanation(
    user_query,
    product
):

    prompt = f"""
You are a product recommendation assistant.

The user asked:
"{user_query}"

The selected product is:

Product: {product.brand} {product.name}
Category: {product.category}
Price: ₹{product.price}
Rating: {product.rating}
RAM: {product.ram}
Storage: {product.storage}
Usage: {product.usage}

Explain briefly why this product is suitable for the user's requirement.

Rules:
1. Use ONLY the product information provided above.
2. Do not invent specifications.
3. Keep the explanation simple.
4. Give 2 or 3 sentences maximum.
"""

    try:

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",

            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },

            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        ).strip()

    except requests.RequestException:

        return "This product matches your selected requirements."        

def parse_ollama_result(result):

    data = {
        "type": "general",
        "category": None,
        "budget": None,
        "usage": "",
        "ram": None,
        "brand": None,
        "answer": "",
    }

    if not result:
        return data

    lines = result.splitlines()

    for line in lines:

        line = line.strip()

        if line.upper().startswith("TYPE:"):

            value = line.split(":", 1)[1].strip().lower()

            if value in ["recommendation", "general"]:
                data["type"] = value


        elif line.upper().startswith("CATEGORY:"):

            value = line.split(":", 1)[1].strip().lower()

            if value in ["mobile", "laptop"]:
                data["category"] = value


        elif line.upper().startswith("BUDGET:"):

            value = line.split(":", 1)[1].strip()

            if value.lower() != "none":

                numbers = re.findall(
                    r"\d+(?:\.\d+)?",
                    value.replace(",", "")
                )

                if numbers:

                    data["budget"] = float(
                        numbers[0]
                    )


        elif line.upper().startswith("USAGE:"):

            value = line.split(":", 1)[1].strip()

            if value.lower() != "none":
                data["usage"] = value.lower()


        elif line.upper().startswith("RAM:"):

            value = line.split(":", 1)[1].strip()

            if value.lower() != "none":

                ram_match = re.search(
                    r"\d+",
                    value
                )

                if ram_match:

                    data["ram"] = int(
                        ram_match.group()
                    )


        elif line.upper().startswith("BRAND:"):

            value = line.split(":", 1)[1].strip()

            if value.lower() != "none":
                data["brand"] = value


        elif line.upper().startswith("ANSWER:"):

            data["answer"] = line.split(
                ":",
                1
            )[1].strip()

    if not data["answer"] and data["type"] == "general":

        answer_lines = []

        for line in lines:

            if ":" not in line:

                if line.strip():

                    answer_lines.append(
                        line.strip()
                    )

        if answer_lines:

            data["answer"] = " ".join(
                answer_lines
            )
    return data


def recommend_product(request):

    query = ""

    recommendations = []

    ai_explanation = ""

    ai_answer = ""

    if request.method == "POST":

        query = request.POST.get(
            "query",
            ""
        ).strip()

        if query:

            # =====================================
            # ASK OLLAMA
            # =====================================

            ollama_result = ask_ollama(query)

            # =====================================
            # PARSE AI RESULT
            # =====================================

            ai_data = parse_ollama_result(
                ollama_result
            )

            # Keep explicit recommendation requests on the catalog path even
            # when the model labels its answer as a general question.
            if re.search(r"\b(recommend|suggest|recommendation)\b", query, re.I):
                ai_data["type"] = "recommendation"

                if not ai_data["category"]:
                    if re.search(r"\b(laptop|notebook)\b", query, re.I):
                        ai_data["category"] = "laptop"
                    elif re.search(r"\b(mobile|phone|smartphone)\b", query, re.I):
                        ai_data["category"] = "mobile"

                if not ai_data["budget"]:
                    budget_match = re.search(
                        r"\b(?:under|below|within)\s*[₹rs.]*\s*([\d,]+)",
                        query,
                        re.I,
                    )
                    if budget_match:
                        ai_data["budget"] = float(
                            budget_match.group(1).replace(",", "")
                        )

            question_type = ai_data["type"]

            category = ai_data["category"]
            budget = ai_data["budget"]
            usage = ai_data["usage"]
            requested_ram = ai_data["ram"]
            brand = ai_data["brand"]
            ai_answer = ai_data["answer"]

            # =====================================
            # GENERAL QUESTION
            # =====================================

            if question_type == "general":

                if not ai_answer:

                    ai_answer = (
                        "I couldn't generate an answer. "
                        "Please try asking your question again."
                    )

            # =====================================
            # PRODUCT RECOMMENDATION
            # =====================================

            else:

                products = Product.objects.filter(
                    is_active=True
                )

                # CATEGORY
                if category:

                    products = products.filter(
                        category=category
                    )

                # BUDGET
                if budget:

                    products = products.filter(
                        price__lte=budget
                    )

                # BRAND
                if brand:

                    products = products.filter(
                        brand__iexact=brand
                    )

                # =================================
                # SCORE PRODUCTS
                # =================================

                scored_products = []

                for product in products:

                    score = 0

                    # RATING
                    if product.rating:

                        score += (
                            float(product.rating) * 10
                        )

                    # BUDGET
                    if budget:

                        if float(product.price) <= budget:

                            score += 20

                    # USAGE
                    if usage and product.usage:

                        usage_text = str(
                            product.usage
                        ).lower()

                        if (
                            usage.lower()
                            in usage_text
                        ):

                            score += 25

                    # RAM
                    if requested_ram and product.ram:

                        product_ram_match = re.search(
                            r"\d+",
                            str(product.ram)
                        )

                        if product_ram_match:

                            product_ram = int(
                                product_ram_match.group(0)
                            )

                            if product_ram >= requested_ram:

                                score += 25

                    # BRAND
                    if brand:

                        if (
                            str(product.brand).lower()
                            == brand.lower()
                        ):

                            score += 20

                    scored_products.append(
                        (
                            product,
                            score
                        )
                    )

                # =================================
                # SORT
                # =================================

                scored_products.sort(
                    key=lambda item: item[1],
                    reverse=True
                )

                # =================================
                # TOP 5
                # =================================

                recommendations = [
                    item[0]
                    for item in scored_products[:5]
                ]

                # =================================
                # BEST PRODUCT EXPLANATION
                # =================================

                if recommendations:

                    best_product = recommendations[0]

                    ai_explanation = generate_ai_explanation(
                        query,
                        best_product
                    )

                else:

                    ai_answer = (
                        "Sorry, I couldn't find a "
                        "matching product in our database."
                    )

    return render(
        request,
        "products/recommend.html",
        {
            "query": query,
            "recommendations": recommendations,
            "ai_explanation": ai_explanation,
            "ai_answer": ai_answer,
        }
    )
# =========================================
# LOGIN
# =========================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.POST.get("next", "")
            if not url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                next_url = "/"

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "redirect": next_url or "/",
                })

            if next_url:
                return redirect(next_url)

            return redirect("/")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": False,
                    "error": "Invalid username or password.",
                },
                status=400,
            )

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "login.html"
    )


# =========================================
# SIGNUP
# =========================================

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "signup.html",
                {
                    "error": "Username already exists."
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/login/")

    return render(
        request,
        "signup.html"
    )    

# =========================================
# LOGOUT
# =========================================

def logout_view(request):

    logout(request)

    return redirect("home")  

# =========================================
# ADD TO CART
# =========================================

@login_required(login_url="/login/")
def add_to_cart(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True
    )

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    count = sum(
        item.quantity
        for item in CartItem.objects.filter(user=request.user)
    )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "cart_count": count,
            "product_name": f"{product.brand} {product.name}",
            "message": "Product added to your cart.",
        })

    return redirect(request.META.get("HTTP_REFERER", "/"))

# =========================================
# CART VIEW
# =========================================

@login_required(login_url="/login/")
def cart_view(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related("product")

    total = 0

    for item in cart_items:

        total += (
            float(item.product.price)
            * item.quantity
        )

    return render(
        request,
        "products/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    ) 

# =========================================
# REMOVE FROM CART
# =========================================

@login_required(login_url="/login/")
def remove_from_cart(request, pk):

    cart_item = get_object_or_404(
        CartItem,
        pk=pk,
        user=request.user
    )

    cart_item.delete()

    return redirect("/cart/")

# =========================================
# UPDATE CART QUANTITY
# =========================================

@login_required(login_url="/login/")
def update_cart_quantity(request, pk, action):

    cart_item = get_object_or_404(
        CartItem,
        pk=pk,
        user=request.user
    )

    if action == "increase":

        cart_item.quantity += 1
        cart_item.save()

    elif action == "decrease":

        if cart_item.quantity > 1:

            cart_item.quantity -= 1
            cart_item.save()

        else:

            cart_item.delete()

    return redirect("/cart/")

def compare_menu(request):
    return render(
        request,
        "products/compare_menu.html"
    )

@login_required(login_url="/login/")
def store_compare_select(request):
    search = request.GET.get("search", "").strip()

    products = Product.objects.filter(is_active=True)

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search)
        )

    return render(
        request,
        "products/store_compare_select.html",
        {
            "products": products,
            "search": search,
        }
    )

@login_required(login_url="/login/")
def store_compare(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True
    )

    store_options, best_option, you_save = build_store_options(product)

    return render(
        request,
        "products/store_compare.html",
        {
            "product": product,
            "store_options": store_options,
            "best_option": best_option,
            "you_save": you_save,
        }
    )

@login_required(login_url="/login/")
def checkout(request):
    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related("product")

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        "products/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )

@login_required(login_url="/login/")
def place_order(request):

    if request.method != "POST":
        return redirect("/checkout/")

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related("product")

    if not cart_items.exists():
        return redirect("/cart/")

    # Customer details
    full_name = request.POST.get("full_name")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    city = request.POST.get("city")
    pincode = request.POST.get("pincode")

    payment_method = request.POST.get(
        "payment_method",
        "Cash on Delivery"
    )

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        full_name=full_name,
        phone=phone,
        address=address,
        city=city,
        pincode=pincode,
        payment_method=payment_method

    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return redirect(
        "order_success"
    )
    
@login_required(login_url="/login/")
def order_success(request):

    return render(
        request,
        "products/order_success.html"
    )

@login_required(login_url="/login/")
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items__product"
    ).order_by("-created_at")

    return render(
        request,
        "products/my_orders.html",
        {
            "orders": orders
        }
    )

@login_required(login_url="/login/")
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "products/order_detail.html",
        {
            "order": order
        }
    )

@login_required(login_url="/login/")
def cancel_order(request, order_id):

    if request.method != "POST":
        return redirect(
            "order_detail",
            order_id=order_id
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status == "pending":
        order.status = "cancelled"
        order.save()

    return redirect(
        "order_detail",
        order_id=order.id
    )

