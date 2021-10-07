from django.core.management.base import BaseCommand
from config.fill import Fill


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        f = Fill()
        f.get_products(1, 100)
        f.clean_products()
        f.create_products_and_categories()
