from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("search/autocomplete/", views.search_autocomplete, name="search_autocomplete"),
    path("category/<slug:slug>/", views.category_detail, name="category"),
    path("<slug:slug>/", views.product_detail, name="product"),
]
