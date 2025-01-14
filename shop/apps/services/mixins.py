from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect

class AuthorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if not(request.user == self.get_object().author or request.user.is_staff):
                messages.info(request, 'Изменение товара доступно только автору!')
                return redirect('home')
            return super().dispatch(request, *args, **kwargs)

class AddProductRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Добавить товар в корзину может только авторизованный пользователь!')
            return redirect('register')
        return super().dispatch(request, *args, **kwargs)

class AddFeedbackRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Для добавления отзыва вы должны быть авторизованы!')
            return redirect('register')
        return super().dispatch(request, *args, **kwargs)

class CreateCartRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Для просмотра и использования корзины \
                          вы должны быть аторизованы!')
            return redirect('register')
        return super().dispatch(request, *args, **kwargs)