import json
from django.shortcuts import render
from django.http import HttpResponse

from product.models import Product


def index(request):
    return render(request, "home/index.html")


def search(request):
    if request.is_ajax():
        query = request.GET.get("term").capitalize()
        products = Product.objects.filter(name__startswith=query)
        results = []
        for product in products:
            results.append(product.name)
        data = json.dumps(results)
    else:
        data = ""
    type = "application/json"
    return HttpResponse(data, type)


def legal(request):
    return render(request, "home/legal.html")


def not_found(request, exception=None):
    return render(request, "home/404.html")
