from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler400, handler403, handler404, handler500


urlpatterns = [
    path("", include("home.urls")),
    path("account/", include("account.urls")),
    path("product/", include("product.urls")),
    path("admin/", admin.site.urls),
]

handler400 = "home.views.not_found"
handler403 = "home.views.not_found"
handler404 = "home.views.not_found"
handler500 = "home.views.not_found"
