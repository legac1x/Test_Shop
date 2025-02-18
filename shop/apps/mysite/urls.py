from django.urls import path # type: ignore
from .views import ProductsListView, ProductDetailView, FeedbackView, ProductFromCategoryView, \
CartItemView, CartListView, ProductCreateView, PrdouctUpdateView, ProceedToCheckoutDetailView, ShopSearch

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('search/', ShopSearch.as_view(), name='shop_search'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/<slug:slug>/update/', PrdouctUpdateView.as_view(), name='product_update'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='products_detail'),
    path('category/<slug:slug>/', ProductFromCategoryView.as_view(), name='products_by_category'),
    path('feedback/<int:id>/', FeedbackView.as_view(), name='feedback'),
    path('cartitem/<int:product_id>/', CartItemView.as_view(), name='cartitem'),
    path('cartlist/<int:cart_id>/', CartListView.as_view(), name='cartlist'),
    path('my/checkout/<int:cart_id>/', ProceedToCheckoutDetailView.as_view(), name='checkout')
]