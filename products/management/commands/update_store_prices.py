from django.core.management.base import BaseCommand
from products.models import Product, ProductOffer


class Command(BaseCommand):

    help = "Update sample Amazon and Flipkart prices"

    def handle(self, *args, **kwargs):

        products = Product.objects.filter(is_active=True)

        for index, product in enumerate(products):

            base_price = float(product.price)

            if index % 2 == 0:
                # Amazon cheaper
                amazon_price = round(base_price * 0.97)
                flipkart_price = round(base_price * 1.01)
            else:
                # Flipkart cheaper
                amazon_price = round(base_price * 1.01)
                flipkart_price = round(base_price * 0.97)

            ProductOffer.objects.update_or_create(
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

            ProductOffer.objects.update_or_create(
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

        self.stdout.write(
            self.style.SUCCESS(
                "Amazon and Flipkart prices updated successfully!"
            )
        )