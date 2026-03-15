from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    products = Product.objects.filter(is_available=True).select_related("category")
    categories = Category.objects.all()
    category_slug = request.GET.get("category")
    query = request.GET.get("q", "")

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "catalog/product_list.html",
        {
            "page_obj": page,
            "categories": categories,
            "current_category": category_slug,
            "query": query,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)

    recently_viewed = request.session.get("recently_viewed", [])
    if product.id not in recently_viewed:
        recently_viewed.insert(0, product.id)
        request.session["recently_viewed"] = recently_viewed[:6]

    return render(request, "catalog/product_detail.html", {"product": product})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "catalog/category_detail.html",
        {
            "category": category,
            "page_obj": page,
        },
    )


def search_autocomplete(request):
    query = request.GET.get("q", "")
    results = []
    if len(query) >= 2:
        products = Product.objects.filter(
            name__icontains=query, is_available=True
        ).values("name", "slug", "price")[:8]
        results = list(products)
    return JsonResponse({"results": results})
