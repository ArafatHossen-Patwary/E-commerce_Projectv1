
from django.urls import path

from . import views

# urlpatterns = [
#     path("", views.home, name="home"),
#     path(
#         "categories/<slug:category_slug>/products",
#         views.category_products,
#         name="category_products",
#     ),
#     path("products/<slug:product_slug>", views.product_detail, name="product_detail"),
#     path(
#         "products/<slug:product_slug>/submit-review",
#         views.submit_view,
#         name="submit_review",
#     ),
# ]

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "categories/<slug:category_slug>/products",
        views.category_products,
        name="category_products",
    ),
    path("products/<slug:product_slug>", views.product_detail, name="product_detail"),
    path(
        "products/<slug:product_slug>/submit-review",
        views.submit_view,
        name="submit_review",
    ),
]



# # urls.py
# from django.urls import path
# from .views import product_list

# urlpatterns = [
#     path("/", product_list, name="product_list"),
#     path("products/", product_list, name="product_list"),
# ]