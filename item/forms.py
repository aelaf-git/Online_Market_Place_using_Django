from django import forms

from .models import Item

INPUT_CLASSES = 'w-full px-5 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 focus:shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all duration-300'

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
        