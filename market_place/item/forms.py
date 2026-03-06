from django import forms

from .models import Item

INPUT_CLASSES = 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Item Name',
                'class': INPUT_CLASSES,
           }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Item Description',
                'class': INPUT_CLASSES,
           }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Price in USD',
                'class': INPUT_CLASSES,
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }
        