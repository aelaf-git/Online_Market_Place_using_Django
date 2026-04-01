from django.http import JsonResponse
from django.conf import settings
from item.models import Item
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
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
            
            # Session-based session_id (use user_id if logged in, else session_key)
            if request.user.is_authenticated:
                session_id = f"user_{request.user.id}"
            else:
                if not request.session.session_key:
                    request.session.create()
                session_id = f"session_{request.session.session_key}"

            # 1. Initialize the LLM
            llm = ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model_name="llama-3.3-70b-versatile"
            )

            # 2. Get Context
            item_context = get_item_context()

            # 3. Create the Prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", 
                 "You are an AI assistant for AELAF MART, a modern online marketplace. "
                 "Your goal is to help users find and buy items. "
                 "Use the following real-time inventory data to answer queries. "
                 "If an item is not in the list, politely inform the user. "
                 "Be helpful, professional, and concise.\n\n"
                 f"{item_context}"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ])

            # 4. Chain with Memory
            chain = prompt | llm

            def get_message_history(session_id: str):
                return PostgresChatMessageHistory(
                    connection_string=settings.DATABASE_URL,
                    session_id=session_id,
                    table_name="chatbot_history"
                )

            chain_with_history = RunnableWithMessageHistory(
                chain,
                get_message_history,
                input_messages_key="input",
                history_messages_key="history",
            )

            # 5. Get Response
            config = {"configurable": {"session_id": session_id}}
            result = chain_with_history.invoke({"input": user_message}, config=config)
            
            return JsonResponse({'response': result.content})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
