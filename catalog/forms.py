from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']
        widgets = {
            'image': forms.FileInput()
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }
