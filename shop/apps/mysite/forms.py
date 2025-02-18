from django import forms
from .models import Feedback, Products


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'body', 'mark']

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['title', 'category', 'price', 'body', 'thumbnail', 'status']

class ProductUpdateForm(ProductCreateForm):
    class Meta:
        model = Products
        fields = ProductCreateForm.Meta.fields

class SearchForm(forms.Form):
    query = forms.CharField()

