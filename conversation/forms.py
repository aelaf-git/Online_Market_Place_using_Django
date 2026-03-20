from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-5 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 focus:shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all duration-300'})
        }