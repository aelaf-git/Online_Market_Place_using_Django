from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from item.models import Item

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)
    active_count = items.filter(is_sold=False).count()
    sold_count = items.filter(is_sold=True).count()
    return render(request, 'dashboard/index.html', {
        'items': items,
        'active_count': active_count,
        'sold_count': sold_count,
    })

