from django.shortcuts import render
from django.core.cache import cache
from catalog.models import Product, Category


def home(request):
    popular = cache.get('popular_products')
    if not popular:
        popular = list(Product.objects.filter(is_popular=True, is_available=True).select_related('category')[:8])
        cache.set('popular_products', popular, 600)

    categories = Category.objects.all()

    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed = Product.objects.filter(id__in=recently_viewed_ids) if recently_viewed_ids else []

    return render(request, 'core/home.html', {
        'popular': popular,
        'categories': categories,
        'recently_viewed': recently_viewed,
    })


def about(request):
    return render(request, 'core/about.html')


def delivery(request):
    return render(request, 'core/delivery.html')


def handler404(request, exception):
    return render(request, 'core/404.html', status=404)
