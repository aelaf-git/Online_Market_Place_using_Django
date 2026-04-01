from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from item.models import Item
from groq import Groq
import json

def get_item_context():
    """Fetch active items and return a summarized string for the LLM."""
    items = Item.objects.filter(is_sold=False)
    context = "Available items in the marketplace:\n"
    for item in items:
        context += f"- {item.name}: ${item.price}. Description: {item.description or 'No description'}\n"
    return context

def chat_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            client = Groq(api_key=settings.GROQ_API_KEY)
            
            item_context = get_item_context()
            
            system_prompt = (
                "You are an AI assistant for AELAF MART, a modern online marketplace. "
                "Your goal is to help users find and buy items. "
                "Use the following real-time inventory data to answer queries. "
                "If an item is not in the list, politely inform the user. "
                "Be helpful, professional, and concise. "
                "The user is currently browsing the site.\n\n"
                f"{item_context}"
            )
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                model="llama-3.3-70b-versatile",
            )
            
            ai_response = chat_completion.choices[0].message.content
            return JsonResponse({'response': ai_response})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
