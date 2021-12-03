from django.core.management.base import BaseCommand
from ...fill import Fill


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        f = Fill()
        f.add_nutriscores()
        f.get_products()
        f.clean_products()
        f.create_products_and_categories()
