# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ReviewForm
from .models import Category, Product, Review


def home(request):

    categories = Category.objects.annotate(product_count=Count("products"))
    context = {"categories": categories}
    return render(request, "products/home.html", context=context)


def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "products": paged_products,
        "category": category,
    }
    return render(request, "products/category_products.html", context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {
        "product": product,
        "rating_counts": 0,
        "rating_percentages": 0,
        "reviews": 0,
    }
    return render(request, "products/product-left-thumbnail.html", context)


@require_POST
@login_required
def submit_view(request, product_slug):
    url = request.META.get("HTTP_REFERER")
    try:
        # Update Existing Review
        review = Review.objects.get(
            user__id=request.user.id, product__slug=product_slug
        )
        form = ReviewForm(request.POST, instance=review)
        form.save()
        messages.success(request, "Thank you! Your review has been updated.")
        return redirect(url)
    except Review.DoesNotExist:

        # Create a Review
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = Review()
            data.product = Product.objects.get(slug=product_slug)
            data.user_id = request.user.id
            data.rating = form.cleaned_data["rating"]
            data.save()
            messages.success(request, "Thank you! Your review has been submitted.")
            return redirect(url)

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product


@login_required
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    

    return redirect("product_detail", product_slug=product.slug)
        

# views.py
from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get("category")
    search = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # Filter by category
    if category_id and category_id.isdigit():
        products = products.filter(category_id=category_id)

    # Search filter
    if search:
        products = products.filter(name__icontains=search)

    # Price filtering
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "products/product_list.html", context)
        