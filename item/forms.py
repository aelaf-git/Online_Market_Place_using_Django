from django import forms

from .models import Item

INPUT_CLASSES = 'w-full px-5 py-3 bg-black border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] transition-colors duration-200'

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

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold')
        widgets = {
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
        