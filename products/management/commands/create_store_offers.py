from django.core.management.base import BaseCommand
from products.models import Product, ProductOffer


class Command(BaseCommand):

    help = "Create sample Amazon and Flipkart offers for all products"

    def handle(self, *args, **kwargs):

        products = Product.objects.filter(is_active=True)

        created_count = 0

        for product in products:

            base_price = float(product.price)

            # Amazon
            amazon_price = round(base_price * 1.02)

            ProductOffer.objects.get_or_create(
                product=product,
                store="Amazon",
                defaults={
                    "price": amazon_price,
                    "rating": 4.5,
                    "delivery": "2-4 days",
                    "offer": "₹1000 off",
                    "product_url": (
                        "https://www.amazon.in/s?k="
                        + product.brand
                        + "+"
                        + product.name
                    ),
                }
            )

            # Flipkart
            flipkart_price = round(base_price * 0.98)

            ProductOffer.objects.get_or_create(
                product=product,
                store="Flipkart",
                defaults={
                    "price": flipkart_price,
                    "rating": 4.4,
                    "delivery": "2-5 days",
                    "offer": "₹1500 off",
                    "product_url": (
                        "https://www.flipkart.com/search?q="
                        + product.brand
                        + "%20"
                        + product.name
                    ),
                }
            )

            created_count += 2

        self.stdout.write(
            self.style.SUCCESS(
                f"Store offers created/checked for {products.count()} products."
            )
        )