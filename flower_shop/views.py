from django.shortcuts import render, get_object_or_404
from flower_shop.models import Bouquet
from django.conf import settings
from django.http import JsonResponse
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_KEY = settings.STRIPE_PUBLIC_KEY 

def view_bouquet(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    return render(request, 'flower_shop/card.html', context={'bouquet': bouquet})


def index(request):
    recommended_bouquets = Bouquet.objects.filter(is_recommended=True)[:3]
    return render(request, 'flower_shop/index.html', context={'recommended_bouquets': recommended_bouquets})


def show_catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'flower_shop/catalog.html', context={'bouquets': bouquets})


def checkout(request):
    return render(request, 'flower_shop/order-step.html', context={'STRIPE_KEY':STRIPE_KEY})

def charge(request):
    if request.method == 'POST':
        amount = 500  
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Оплата заказа',
                source=request.POST['stripeToken']
            )
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)})
        except Exception as e:
            return JsonResponse({'error': str(e)})