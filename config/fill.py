import requests

from product.models import Product, Category


class Fill:
    products = []
    cleaned_products = []

    def get_products(self, max_page=10, page_size=1000):
        """Method used to loop OpenFoodFacts request to get products data."""

        page_nb = 1
        while page_nb <= max_page:
            params = {
                "action": "process",
                "tagtype_0": "categories",
                "tagtype_1": "countries",
                "tag_contains_1": "france",
                "fields": "categories,categories_lc,brands,generic_name_fr,image_url,nutrition_grade_fr,product_name,stores,url",
                "page_size": page_size,
                "page": page_nb,
                "json": 1,
            }

            products_url = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl", params=params
            )

            self.products.extend(products_url.json()["products"])
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
            if not product.description:
                continue

            # Get product brand
            product.brands = item.get("brands", "")
            if not product.brands:
                continue

            # Get product store
            product.stores = item.get("stores", "")

            # Get product nutriscore
            product.nutriscore = item.get("nutrition_grade_fr")
            if not product.nutriscore:
                continue

            # Get product URL
            product.url = item.get("url", "")
            if not product.url:
                continue

            # Get product image URL
            product.image_url = item.get("image_url", "")
            if not product.image_url:
                continue

            self.cleaned_products.append((product, categories))

    def create_products_and_categories(self):
        """Method used to insert products and categories in database."""

        try:
            for item in self.cleaned_products:
                product = item[0]
                prod, created = Product.objects.get_or_create(
                    name=product.name,
                    defaults={
                        "description": product.description,
                        "brands": product.brands,
                        "stores": product.stores,
                        "nutriscore": product.nutriscore,
                        "url": product.url,
                        "image_url": product.image_url,
                    },
                )

                for category in item[1]:
                    print(category)
                    cat, created = Category.objects.get_or_create(name=category)
                    prod.categories.add(cat)
        except Exception as e:
            raise (e)
