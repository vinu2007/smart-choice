from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    CATEGORY_CHOICES = [
        ("mobile", "Mobile"),
        ("laptop", "Laptop"),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    name = models.CharField(
        max_length=200
    )

    brand = models.CharField(
        max_length=100
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True
    )

    ram = models.CharField(
        max_length=50,
        blank=True
    )

    storage = models.CharField(
        max_length=100,
        blank=True
    )

    processor = models.CharField(
        max_length=150,
        blank=True
    )

    battery = models.CharField(
        max_length=100,
        blank=True
    )

    display = models.CharField(
        max_length=150,
        blank=True
    )

    gpu = models.CharField(
        max_length=150,
        blank=True
    )

    camera = models.CharField(
        max_length=150,
        blank=True
    )

    usage = models.CharField(
        max_length=200,
        blank=True
    )

    source = models.CharField(
        max_length=200,
        default="Local Database"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.brand} {self.name}"


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    store = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )
    delivery = models.CharField(max_length=100, blank=True)
    offer = models.CharField(max_length=200, blank=True)
    product_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.store}"

class CartItem(models.Model):

    user = models.ForeignKey(
         User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    full_name = models.CharField(
        max_length=100,
        default=""
    )

    phone = models.CharField(
        max_length=15,
        default=""
    )

    address = models.TextField(
        default=""
    )
    
    city = models.CharField(
        max_length=100,
        default=""
    )

    pincode = models.CharField(
        max_length=10,
        default=""
    )

    payment_method = models.CharField(
        max_length=30,
        default="Cash on Delivery"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.order.id} - {self.product.name}"