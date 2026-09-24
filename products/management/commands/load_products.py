from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):

    help = "Load 25 mobile and 25 laptop products"

    def handle(self, *args, **kwargs):

        products = [

            # =========================
            # 📱 MOBILE PRODUCTS - 25
            # =========================

            {
                "name": "Galaxy S25",
                "brand": "Samsung",
                "category": "mobile",
                "price": 74999,
                "rating": 4.6,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 8 Elite",
                "usage": "gaming"
            },

            {
                "name": "Galaxy A56",
                "brand": "Samsung",
                "category": "mobile",
                "price": 41999,
                "rating": 4.4,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Exynos 1580",
                "usage": "daily use"
            },

            {
                "name": "Galaxy A36",
                "brand": "Samsung",
                "category": "mobile",
                "price": 32999,
                "rating": 4.3,
                "ram": "8 GB",
                "storage": "128 GB",
                "processor": "Snapdragon 6 Gen 3",
                "usage": "daily use"
            },

            {
                "name": "iPhone 16",
                "brand": "Apple",
                "category": "mobile",
                "price": 79900,
                "rating": 4.7,
                "ram": "8 GB",
                "storage": "128 GB",
                "processor": "Apple A18",
                "usage": "camera"
            },

            {
                "name": "iPhone 16 Plus",
                "brand": "Apple",
                "category": "mobile",
                "price": 89900,
                "rating": 4.7,
                "ram": "8 GB",
                "storage": "128 GB",
                "processor": "Apple A18",
                "usage": "camera"
            },

            {
                "name": "iPhone 15",
                "brand": "Apple",
                "category": "mobile",
                "price": 69900,
                "rating": 4.6,
                "ram": "6 GB",
                "storage": "128 GB",
                "processor": "Apple A16 Bionic",
                "usage": "daily use"
            },

            {
                "name": "OnePlus 13",
                "brand": "OnePlus",
                "category": "mobile",
                "price": 69999,
                "rating": 4.7,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 8 Elite",
                "usage": "gaming"
            },

            {
                "name": "OnePlus 13R",
                "brand": "OnePlus",
                "category": "mobile",
                "price": 42999,
                "rating": 4.6,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 8 Gen 3",
                "usage": "gaming"
            },

            {
                "name": "Nord 5",
                "brand": "OnePlus",
                "category": "mobile",
                "price": 34999,
                "rating": 4.4,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 8s Gen 3",
                "usage": "gaming"
            },

            {
                "name": "Pixel 9",
                "brand": "Google",
                "category": "mobile",
                "price": 79999,
                "rating": 4.6,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Google Tensor G4",
                "usage": "camera"
            },

            {
                "name": "Pixel 9a",
                "brand": "Google",
                "category": "mobile",
                "price": 49999,
                "rating": 4.5,
                "ram": "8 GB",
                "storage": "128 GB",
                "processor": "Google Tensor G4",
                "usage": "camera"
            },

            {
                "name": "Xiaomi 15",
                "brand": "Xiaomi",
                "category": "mobile",
                "price": 64999,
                "rating": 4.5,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 8 Elite",
                "usage": "gaming"
            },

            {
                "name": "Redmi Note 14 Pro",
                "brand": "Xiaomi",
                "category": "mobile",
                "price": 29999,
                "rating": 4.3,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Dimensity 7300 Ultra",
                "usage": "camera"
            },

            {
                "name": "Poco X7 Pro",
                "brand": "Poco",
                "category": "mobile",
                "price": 27999,
                "rating": 4.4,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Dimensity 8400 Ultra",
                "usage": "gaming"
            },

            {
                "name": "Realme GT 7",
                "brand": "Realme",
                "category": "mobile",
                "price": 39999,
                "rating": 4.5,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Dimensity 9400e",
                "usage": "gaming"
            },

            {
                "name": "Realme 14 Pro+",
                "brand": "Realme",
                "category": "mobile",
                "price": 29999,
                "rating": 4.3,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 7s Gen 3",
                "usage": "camera"
            },

            {
                "name": "Vivo V50",
                "brand": "Vivo",
                "category": "mobile",
                "price": 34999,
                "rating": 4.4,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 7 Gen 3",
                "usage": "camera"
            },

            {
                "name": "Vivo X200",
                "brand": "Vivo",
                "category": "mobile",
                "price": 65999,
                "rating": 4.6,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Dimensity 9400",
                "usage": "camera"
            },

            {
                "name": "Reno 13",
                "brand": "Oppo",
                "category": "mobile",
                "price": 37999,
                "rating": 4.4,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Dimensity 8350",
                "usage": "camera"
            },

            {
                "name": "Find X8",
                "brand": "Oppo",
                "category": "mobile",
                "price": 69999,
                "rating": 4.6,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Dimensity 9400",
                "usage": "camera"
            },

            {
                "name": "Edge 60",
                "brand": "Motorola",
                "category": "mobile",
                "price": 29999,
                "rating": 4.3,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Dimensity 7400",
                "usage": "daily use"
            },

            {
                "name": "Moto G85",
                "brand": "Motorola",
                "category": "mobile",
                "price": 19999,
                "rating": 4.2,
                "ram": "8 GB",
                "storage": "128 GB",
                "processor": "Snapdragon 6s Gen 3",
                "usage": "daily use"
            },

            {
                "name": "Phone 3a",
                "brand": "Nothing",
                "category": "mobile",
                "price": 27999,
                "rating": 4.3,
                "ram": "8 GB",
                "storage": "128 GB",
                "processor": "Snapdragon 7s Gen 3",
                "usage": "daily use"
            },

            {
                "name": "Neo 10",
                "brand": "iQOO",
                "category": "mobile",
                "price": 32999,
                "rating": 4.5,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 8s Gen 4",
                "usage": "gaming"
            },

            {
                "name": "iQOO 13",
                "brand": "iQOO",
                "category": "mobile",
                "price": 54999,
                "rating": 4.6,
                "ram": "12 GB",
                "storage": "256 GB",
                "processor": "Snapdragon 8 Elite",
                "usage": "gaming"
            },


            # =========================
            # 💻 LAPTOP PRODUCTS - 25
            # =========================

            {
                "name": "Inspiron 15",
                "brand": "Dell",
                "category": "laptop",
                "price": 57990,
                "rating": 4.3,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "study"
            },

            {
                "name": "Inspiron 14",
                "brand": "Dell",
                "category": "laptop",
                "price": 62990,
                "rating": 4.4,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "development"
            },

            {
                "name": "G15 Gaming",
                "brand": "Dell",
                "category": "laptop",
                "price": 89990,
                "rating": 4.5,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i7",
                "usage": "gaming"
            },

            {
                "name": "HP 15s",
                "brand": "HP",
                "category": "laptop",
                "price": 54990,
                "rating": 4.2,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "study"
            },

            {
                "name": "Pavilion 14",
                "brand": "HP",
                "category": "laptop",
                "price": 64990,
                "rating": 4.4,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "development"
            },

            {
                "name": "Victus 15",
                "brand": "HP",
                "category": "laptop",
                "price": 74990,
                "rating": 4.5,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "AMD Ryzen 7",
                "usage": "gaming"
            },

            {
                "name": "Omen 16",
                "brand": "HP",
                "category": "laptop",
                "price": 119990,
                "rating": 4.7,
                "ram": "16 GB",
                "storage": "1 TB",
                "processor": "Intel Core i7",
                "usage": "gaming"
            },

            {
                "name": "IdeaPad Slim 3",
                "brand": "Lenovo",
                "category": "laptop",
                "price": 48990,
                "rating": 4.2,
                "ram": "8 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "study"
            },

            {
                "name": "IdeaPad Slim 5",
                "brand": "Lenovo",
                "category": "laptop",
                "price": 69990,
                "rating": 4.5,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "AMD Ryzen 7",
                "usage": "development"
            },

            {
                "name": "LOQ 15",
                "brand": "Lenovo",
                "category": "laptop",
                "price": 84990,
                "rating": 4.6,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i7",
                "usage": "gaming"
            },

            {
                "name": "Legion 5",
                "brand": "Lenovo",
                "category": "laptop",
                "price": 109990,
                "rating": 4.7,
                "ram": "16 GB",
                "storage": "1 TB",
                "processor": "AMD Ryzen 7",
                "usage": "gaming"
            },

            {
                "name": "Vivobook 15",
                "brand": "ASUS",
                "category": "laptop",
                "price": 56990,
                "rating": 4.3,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "study"
            },

            {
                "name": "Vivobook 16",
                "brand": "ASUS",
                "category": "laptop",
                "price": 64990,
                "rating": 4.4,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "development"
            },

            {
                "name": "TUF Gaming F15",
                "brand": "ASUS",
                "category": "laptop",
                "price": 79990,
                "rating": 4.5,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i7",
                "usage": "gaming"
            },

            {
                "name": "ROG Strix G16",
                "brand": "ASUS",
                "category": "laptop",
                "price": 129990,
                "rating": 4.8,
                "ram": "16 GB",
                "storage": "1 TB",
                "processor": "Intel Core i9",
                "usage": "gaming"
            },

            {
                "name": "Aspire 5",
                "brand": "Acer",
                "category": "laptop",
                "price": 54990,
                "rating": 4.3,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "study"
            },

            {
                "name": "Aspire Lite",
                "brand": "Acer",
                "category": "laptop",
                "price": 44990,
                "rating": 4.1,
                "ram": "8 GB",
                "storage": "512 GB",
                "processor": "AMD Ryzen 5",
                "usage": "study"
            },

            {
                "name": "Nitro V",
                "brand": "Acer",
                "category": "laptop",
                "price": 74990,
                "rating": 4.5,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "gaming"
            },

            {
                "name": "Predator Helios Neo 16",
                "brand": "Acer",
                "category": "laptop",
                "price": 119990,
                "rating": 4.7,
                "ram": "16 GB",
                "storage": "1 TB",
                "processor": "Intel Core i7",
                "usage": "gaming"
            },

            {
                "name": "Modern 14",
                "brand": "MSI",
                "category": "laptop",
                "price": 59990,
                "rating": 4.3,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "development"
            },

            {
                "name": "Thin 15",
                "brand": "MSI",
                "category": "laptop",
                "price": 69990,
                "rating": 4.4,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Intel Core i5",
                "usage": "gaming"
            },

            {
                "name": "Katana 15",
                "brand": "MSI",
                "category": "laptop",
                "price": 89990,
                "rating": 4.6,
                "ram": "16 GB",
                "storage": "1 TB",
                "processor": "Intel Core i7",
                "usage": "gaming"
            },

            {
                "name": "MacBook Air M2",
                "brand": "Apple",
                "category": "laptop",
                "price": 89990,
                "rating": 4.7,
                "ram": "8 GB",
                "storage": "256 GB",
                "processor": "Apple M2",
                "usage": "development"
            },

            {
                "name": "MacBook Air M3",
                "brand": "Apple",
                "category": "laptop",
                "price": 99990,
                "rating": 4.8,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Apple M3",
                "usage": "development"
            },

            {
                "name": "MacBook Pro M3",
                "brand": "Apple",
                "category": "laptop",
                "price": 169990,
                "rating": 4.9,
                "ram": "16 GB",
                "storage": "512 GB",
                "processor": "Apple M3 Pro",
                "usage": "professional"
            },
        ]

        created = 0
        skipped = 0

        for data in products:

            product, created_now = Product.objects.get_or_create(
                name=data["name"],
                brand=data["brand"],
                defaults={
                    **data,
                    "is_active": True,
                }
            )

            if created_now:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Products created: {created}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"⏭️ Products already existed: {skipped}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"📦 Total products in database: {Product.objects.count()}"
            )
        )