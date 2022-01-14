from product.fill import Fill

def fill():
    f = Fill()
    f.add_nutriscores()
    f.get_products()
    f.clean_products()
    f.create_products_and_categories()
