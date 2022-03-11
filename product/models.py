from django.db import models
from django.db.models.deletion import CASCADE

from account.models import User


class Nutriscore(models.Model):
    nutriscore = models.CharField(max_length=1, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    brands = models.CharField(max_length=200)
    stores = models.CharField(max_length=200)
    nutriscore = models.ForeignKey(Nutriscore, on_delete=CASCADE, default=None)
    url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    image_nutrition_url = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)

    def get_product(product_name):
        products = Product.objects.filter(name__icontains=product_name)

        try:
            product = products[0]
        except:
            return None
        else:
            return product

    def find_substitute(product):
        substitutes = []
        filtered_substitutes = []
        categories = product.categories.all()

        targeted_category = ""
        targeted_category_count = 0
        for category in categories:
            category_count = len(
                Product.objects.filter(categories__name__icontains=category.name)
            )

            if targeted_category:
                if category_count < targeted_category_count:
                    targeted_category = category
                    targeted_category_count = category_count
            else:
                targeted_category = category
                targeted_category_count = category_count

        substitutes = Product.objects.filter(
            categories__name__icontains=targeted_category.name
        )
        substitutes = list(set(substitutes))
        substitutes = sorted(
            substitutes, key=lambda prod: ord(prod.nutriscore.nutriscore)
        )

        for substitute in substitutes:
            if (
                len(filtered_substitutes) < 30
                and substitute != product
                and ord(substitute.nutriscore.nutriscore)
                <= ord(product.nutriscore.nutriscore)
            ):
                filtered_substitutes.append(substitute)

        return filtered_substitutes


class Substitute(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE, related_name="product")
    substitute = models.ForeignKey(
        Product, on_delete=CASCADE, related_name="substitute"
    )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]
