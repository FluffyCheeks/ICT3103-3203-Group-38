from django import forms
from .models import Product_Details


class PDForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Product_Details
        fields = ('name','image')
        # fields = ('category_id', 'name','description', 'image', 'ingredients', 'unit_price', 'stock_available', 'slug')