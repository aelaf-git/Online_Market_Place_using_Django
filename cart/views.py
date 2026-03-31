import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from item.models import Item
from .models import Cart, CartItem, Order

# stripe.api_key = settings.STRIPE_SECRET_KEY # Removed from here

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id, is_sold=False)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart:view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view.html', {
        'cart': cart
    })

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')

@login_required
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        return redirect('cart:view_cart')
    
    line_items = []
    for cart_item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': cart_item.item.name,
                },
                'unit_amount': int(cart_item.item.price * 100),
            },
            'quantity': cart_item.quantity,
        })
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('cart:success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('cart:cancel')),
            metadata={
                'user_id': request.user.id,
                'cart_id': cart.id
            }
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            handle_checkout_session(session)
            
    return render(request, 'cart/success.html')

@login_required
def cancel(request):
    return render(request, 'cart/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return HttpResponse(status=200)

from conversation.models import Conversation, ConversationMessage
from django.contrib.auth.models import User

def handle_checkout_session(session):
    user_id = session['metadata']['user_id']
    cart_id = session['metadata']['cart_id']
    
    cart = Cart.objects.get(id=cart_id)
    order = Order.objects.create(
        user_id=user_id,
        total_amount=session['amount_total'] / 100,
        stripe_payment_intent_id=session['payment_intent'],
        is_paid=True
    )
    
    superuser = User.objects.filter(is_superuser=True).first()
    
    for cart_item in cart.items.all():
        order.items.add(cart_item.item)
        cart_item.item.is_sold = True
        cart_item.item.save()
        
        # Send message to seller from superuser
        if superuser:
            # Look for an existing conversation between superuser and seller regarding this item
            conversation = Conversation.objects.filter(item=cart_item.item).filter(members__id=superuser.id).filter(members__id=cart_item.item.created_by.id).first()
            
            if not conversation:
                conversation = Conversation.objects.create(item=cart_item.item)
                conversation.members.add(superuser)
                conversation.members.add(cart_item.item.created_by)
            
            ConversationMessage.objects.create(
                conversation=conversation,
                content=f"Congratulations! Your item '{cart_item.item.name}' has been sold for ${cart_item.item.price}. Please check your dashboard for details and prepare the item for delivery.",
                created_by=superuser
            )
        
    cart.items.all().delete()
