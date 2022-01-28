from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Substitute


def search(request):
    context = {}

    if request.method == "POST":
        product_name = request.POST.get("search-request")
    else:
        product_name = request.GET.get("product")

    if product_name:
        product = Product.get_product(product_name)

        if product:
            substitutes = Product.find_substitute(product)
            paginator = Paginator(substitutes, 6)
            page = request.GET.get("page")

            try:
                substitutes_in_page = paginator.page(page)
            except PageNotAnInteger:
                substitutes_in_page = paginator.page(1)
            except EmptyPage:
                substitutes_in_page = paginator.page(paginator.num_pages)

            for substitute in substitutes_in_page:
                try:
                    user = request.user
                    Substitute.objects.get(user=user, substitute=substitute)
                    substitute.saved = True
                except Substitute.DoesNotExist:
                    pass

            context = {
                "product": product,
                "substitutes": substitutes_in_page,
            }

            return render(request, "product/search.html", context)
    return render(request, "home/404.html", status=404)


def details(request, product_name=None):
    try:
        product = Product.objects.get(name=product_name)
    except Product.DoesNotExist:
        return render(request, "home/404.html", status=404)
    else:
        context = {
            "product": product,
            "nutriscore_img": f"nutriscore-{product.nutriscore.nutriscore}.png",
        }

        return render(request, "product/details.html", context)


def substitutes(request):
    substitutes = Substitute.objects.filter(user=request.user)
    paginator = Paginator(substitutes, 6)
    page = request.GET.get("page")

    try:
        substitutes_in_page = paginator.page(page)
    except PageNotAnInteger:
        substitutes_in_page = paginator.page(1)
    except EmptyPage:
        substitutes_in_page = paginator.page(paginator.num_pages)

    context = {
        "substitutes": substitutes_in_page,
    }

    return render(request, "product/substitutes.html", context)


@login_required(login_url="login")
def save(request):
    if request.method == "POST":
        user = request.user
        query = request.POST["save"]
        query_list = query.split(",")
        product_name = query_list[0]
        substitute_id = query_list[1]
        product = Product.objects.get(name=product_name)
        substitute = Product.objects.get(id=substitute_id)

        for saved_substitute in user.substitute_set.all():
            if saved_substitute.substitute.name == substitute.name:
                return redirect("/product/substitutes/")

        Substitute.objects.create(user=user, product=product, substitute=substitute)

    return redirect("/product/substitutes/")


@login_required(login_url="login")
def delete(request):
    if request.method == "POST":
        user = request.user
        substitute = Substitute.objects.get(
            user=user, substitute__name=request.POST["substitute"]
        )
        substitute.delete()
    return redirect("/product/substitutes/")
