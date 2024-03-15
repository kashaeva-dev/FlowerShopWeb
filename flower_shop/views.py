from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers

from flower_shop.forms import ConsultingForm
from flower_shop.models import Bouquet, ConsultingStatus, ConsultingStatusHistory
from django.conf import settings
from django.http import JsonResponse
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_KEY = settings.STRIPE_PUBLIC_KEY 

def view_bouquet(request, bouquet_id):
    form = ConsultingForm()
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    return render(request, 'flower_shop/card.html', context={'bouquet': bouquet})


def index(request):
    form = ConsultingForm()
    recommended_bouquets = Bouquet.objects.filter(is_recommended=True)[:3]
    return render(request, 'flower_shop/index.html', context={'recommended_bouquets': recommended_bouquets,
                                                              'form': form,
                                                              })


def show_catalog(request):
    form = ConsultingForm()
    all_bouquets = Bouquet.objects.all()
    paginator = Paginator(all_bouquets, 6)
    bouquets = paginator.get_page(1)
    return render(request, 'flower_shop/catalog.html', context={'bouquets': bouquets, 'form': form})


def consultation(request):
    return render(request, 'flower_shop/consultation.html')


def consulting_request(request):
    if request.method == 'POST':
        form = ConsultingForm(request.POST)
        if form.is_valid():
            try:
                consulting = form.save(commit=False)
                consulting.save()
                consulting_status = ConsultingStatus.objects.get(pk=1)
                ConsultingStatusHistory.objects.create(consulting=consulting,
                                                           status=consulting_status)
            except Exception:
                return render(request, 'flower_shop/consultation_request_fail.html')
            return render(request, 'flower_shop/consultation_request_success.html',
                          context={'consultation': consulting})
    else:
        form = ConsultingForm()
    return render(request, 'flower_shop/consultation.html', {'form': form})


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


def bouquet_list_ajax(request):
    all_bouquets = Bouquet.objects.all()
    paginator = Paginator(all_bouquets, 6)

    page_number = request.GET.get('page')
    bouquets = paginator.get_page(page_number)

    bouquets_serialized = serializers.serialize('json', bouquets)

    return JsonResponse({
        'bouquets': bouquets_serialized,
        'has_next': bouquets.has_next(),
        'next_page_number': bouquets.next_page_number() if bouquets.has_next() else '',
    })
