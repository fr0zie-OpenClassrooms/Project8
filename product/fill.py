import requests

from product.models import Product, Category, Nutriscore


class Fill:
    def __init__(self):
        self.raw_products = []
        self.products = []
        self.cleaned_products = []

    def add_nutriscores(self):
        nutriscores = ["a", "b", "c", "d", "e"]
        for nutriscore in nutriscores:
            nutriscore, created = Nutriscore.objects.get_or_create(
                nutriscore=nutriscore
            )

    def get_products(self, max_page=10, page_size=1000):
        """Method used to loop OpenFoodFacts request to get products data."""

        page_nb = 1
        while page_nb <= max_page:
            params = {
                "action": "process",
                "tagtype_0": "categories",
                "tagtype_1": "countries",
                "tag_contains_1": "france",
                "fields": "categories,categories_lc,brands,generic_name_fr,image_url,image_nutrition_url,nutrition_grade_fr,product_name,stores,url",
                "page_size": page_size,
                "page": page_nb,
                "json": 1,
            }

            self.raw_products = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl", params=params
            )

            self.products.extend(self.raw_products.json()["products"])
            page_nb += 1

    def clean_products(self):
        """Method used to clean products and categories."""

        for item in self.products:
            product = Product()

            # Check if category language is french
            category_language = item.get("categories_lc")
            if category_language != "fr":
                continue

            # Get product categories
            categories = [item for item in item["categories"].strip(" ").split(",")]
            if not categories:
                continue

            # Get product name
            product.name = item.get("product_name", "")
            if not product.name or product.name == "Chargement...":
                continue

            # Get product description
            product.description = item.get("generic_name_fr", "")

            # Get product brand
            product.brands = item.get("brands", "")

            # Get product store
            product.stores = item.get("stores", "")

            # Get product nutriscore
            # Erreur dans Test
            try:
                product.nutriscore = Nutriscore.objects.get(
                    nutriscore=item.get("nutrition_grade_fr")
                )
            except:
                continue

            # Get product URL
            product.url = item.get("url", "")
            if not product.url:
                continue

            # Get product image URL
            product.image_url = item.get("image_url", "")
            if not product.image_url:
                continue

            # Get product nutrition image URL
            product.image_nutrition_url = item.get("image_nutrition_url", "")
            if not product.image_nutrition_url:
                continue

            self.cleaned_products.append((product, categories))

    def create_products_and_categories(self):
        """Method used to insert products and categories in database."""

        for product, categories in self.cleaned_products:
            try:
                prod, created = Product.objects.get_or_create(
                    name=product.name,
                    defaults={
                        "description": product.description,
                        "brands": product.brands,
                        "stores": product.stores,
                        "nutriscore": product.nutriscore,
                        "url": product.url,
                        "image_url": product.image_url,
                        "image_nutrition_url": product.image_nutrition_url,
                    },
                )

                for category in categories:
                    cat, created = Category.objects.get_or_create(name=category)
                    prod.categories.add(cat)
            except:
                pass
