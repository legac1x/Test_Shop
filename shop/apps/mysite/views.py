from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView
from .models import Products, Category, Cart, CartItem
from .forms import FeedbackForm, ProductCreateForm, ProductUpdateForm, SearchForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from ..services.mixins import AuthorRequiredMixin, AddProductRequiredMixin, \
AddFeedbackRequiredMixin, CreateCartRequiredMixin
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector, TrigramSimilarity

class CartListView(CreateCartRequiredMixin, ListView):
    '''Просмотр корзины'''
    template_name = 'products/cart_list_view.html'
    context_object_name = 'products'

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user.id)
        if cart:
            items = CartItem.objects.filter(cart_id=cart.id)
            items = items.values_list('item_id', flat=True)
            items = Products.custom.filter(id__in=items)
            return items
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user.id)
        items = CartItem.objects.filter(cart_id=cart.id)
        items = items.values_list('item_id', flat=True)
        items = Products.custom.filter(id__in=items)
        total_sum = sum([int(''.join(x.price.split())) for x in items])
        context['title'] = 'Корзина'
        context['cart'] = cart
        context['total_sum'] = total_sum
        return context

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(id=self.kwargs.get('cart_id'))
        item = Products.custom.get(id=self.request.POST.get('product_id'))
        if cart:
            cart_item = CartItem.objects.get(cart_id=cart.id, item_id=item.id)
            cart_item.delete()
        return redirect('cartlist', cart_id=cart.id)

class ProductsListView(ListView):
    '''Просмотр каталога товаров'''
    model = Products
    context_object_name = 'products'
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        cached_products = cache.get("products_list")
        if cached_products:
            return cached_products
        else:
            queryset = super().get_queryset()
            cache.set("products_list", queryset, timeout=600)
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_categories = Category.objects.filter(parent=None)
        context['parent_categories'] = parent_categories
        context['title'] = 'Главная страница'
        return context

class ProductDetailView(DetailView):
    '''Детальный просмотр товара'''
    model = Products
    template_name = 'products/products_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['form'] = FeedbackForm()
        product = get_object_or_404(Products, status='present', slug=self.kwargs.get('slug'))
        feedbacks = product.feedbacks.all()
        context['feedbacks'] = feedbacks
        return context

class FeedbackView(AddFeedbackRequiredMixin, View):
    '''Отзывы'''
    template_name = 'products/feedback.html'
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Products, status='present', id=self.kwargs.get('id'))
        form = FeedbackForm(request.POST)
        feedback = None
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.product = product
            feedback.save()
            return render(request, self.template_name, {'form': form,
                                                        'product': product,
                                                        'feedback': feedback})
        return render(request, self.template_name, {'form': form,
                                                    'product': product,
                                                    'feedback': feedback})

class ProductFromCategoryView(ListView):
    '''Товары по категорям'''
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    category = None
    paginate_by = 6

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs.get('slug'))
        parent = self.category.parent
        if parent is not None:
            queryset = Products.custom.filter(category__in=self.category.get_descendants(include_self=True))
            return queryset
        else:
            sub_cat = self.category.get_descendants(include_self=True)
            queryset = Products.custom.filter(category__in=sub_cat)
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('slug')
        context['title'] = f'Товары из категории: {self.category.title}'
        if cat_slug:
            category = Category.objects.get(slug=cat_slug)
            context['cat_slug'] = category
            sub_cat = Category.objects.filter(parent=category)
            parent_cat = category.parent
            if sub_cat:
                context['sub_cat'] = sub_cat
            if parent_cat:
                context['parent_cat'] = parent_cat
        return context


class CartItemView(AddProductRequiredMixin, View):
    '''Добавление товара в корзину'''
    def post(self, request, *args, **kwargs):
        product = Products.custom.get(id=self.kwargs.get('product_id'))
        cart = Cart.objects.get(user=self.request.user.id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item_id=product.id)
        if not created:
            cart_item.save()
        return redirect('products_detail', slug=product.slug)

class ProductCreateView(LoginRequiredMixin,CreateView):
    '''Добавление своего товара на маркетплейс'''
    model = Products
    template_name = 'products/create_product.html'
    form_class = ProductCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class PrdouctUpdateView(AuthorRequiredMixin, UpdateView, SuccessMessageMixin):
    '''Обновление своего товара'''
    model = Products
    template_name = 'products/product_update.html'
    context_object_name = 'product'
    form_class = ProductUpdateForm
    login_url = 'home'
    success_message = f'Запись была успешно обновлена!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи {self.object.title}'
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)

class ProceedToCheckoutDetailView(View):
    '''Перейти к оформлению'''
    template_name = 'products/checkout.html'

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user.id)
        items = CartItem.objects.filter(cart_id=cart.id)
        items = items.values_list('item_id', flat=True)
        items = Products.custom.filter(id__in=items)
        total_sum = sum([int(''.join(x.price.split())) for x in items])

        context = {
            'title': 'Оформление заказа',
            'cart': cart,
            'total_sum': total_sum,
            'items': items
        }
        return render(request, self.template_name, context)

class ShopSearch(View):
    '''Полнотекстовый поиск'''
    form = SearchForm()
    query = None
    results = []

    def get(self, request, *args, **kwargs):
        if 'query' in request.GET:
            self.form = SearchForm(request.GET)

            if self.form.is_valid():
                self.query = self.form.cleaned_data['query']
                self.results = Products.custom.annotate(
                    similarity=TrigramSimilarity('title', self.query),
                ).filter(similarity__gte=0.05).order_by('-similarity')
        return render(request, 'products/includes/search.html', {'form': self.form,
                                                        'query': self.query,
                                                        'results': self.results})