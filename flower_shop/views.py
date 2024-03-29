import datetime

from django.core.paginator import Paginator

from django.shortcuts import get_list_or_404, redirect

from flower_shop.forms import OrderForm
from flower_shop.models import Occasion, Order

from django.shortcuts import render, get_object_or_404
from django.core import serializers

from flower_shop.forms import ConsultingForm
from flower_shop.models import Bouquet, ConsultingStatus, ConsultingStatusHistory

from django.conf import settings
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_KEY = settings.STRIPE_PUBLIC_KEY


def create_order(request, bouquet_id):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST, bouquet_id=bouquet_id)
        if form.is_valid():
            order = form.save_order()
            order.status = 'new'
            order.delivery_date = order.created_at
            order.save()
            if order.payment_type.name == 'наличными курьеру':
                return render(request, 'flower_shop/result.html', context={'order': order})
            return render(request, 'flower_shop/order-step.html', context={
                'STRIPE_KEY': STRIPE_KEY,
                'order': order
            })
    return render(request, 'flower_shop/order.html', context={'form': form,
                                                              'bouquet_id': bouquet_id,
                                                              })


def find_bouquet(request):
    form = ConsultingForm()
    bouquets = None
    if 'event' in request.GET and 'price' in request.GET:
        price_range = request.GET['price']
        event_id = request.GET['event']

        if price_range == "None":
            price_range = None
        else:
            price_range = tuple(map(int, price_range.split('-')))

        bouquets = Bouquet.objects.filter(occasion__id=event_id)

        if price_range is not None and len(price_range) == 2:
            bouquets = bouquets.filter(price__range=(price_range[0], price_range[1]))

        paginator = Paginator(bouquets, 6)
        bouquets = paginator.get_page(1)
        has_next = bouquets.has_next() if bouquets.has_next() else ''

        return render(request, 'flower_shop/catalog.html',
                      context={'bouquets': bouquets,
                               'form': form,
                               'caption': 'Вам подойдут букеты',
                                'has_next': has_next,
                               'filters': f'event={event_id}&price={request.GET["price"]}',
                               })

    if 'event' in request.GET:
        context = {'price': {'До 1000 руб.': '0-1000',
                             '1000-5000 руб.': '1000-5000',
                             'от 5000 руб.': '5000-1000000',
                             'Не имеет значения': None}}
        event = request.GET['event']
        context['event'] = event
        return render(request, 'flower_shop/quiz-step.html', context=context)

    occasions = get_list_or_404(Occasion)
    return render(request, 'flower_shop/quiz.html', context={'occasions': occasions})


def view_bouquet(request, bouquet_id):
    form = ConsultingForm()
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    return render(request, 'flower_shop/card.html', context={'bouquet': bouquet, 'form': form})


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
    has_next = bouquets.has_next() if bouquets.has_next() else ''
    return render(request, 'flower_shop/catalog.html', context={'bouquets': bouquets,
                                                                'form': form,
                                                                'caption': 'Все букеты',
                                                                'has_next': has_next,
                                                                })


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
    return render(request, 'flower_shop/order-step.html', context={'STRIPE_KEY': STRIPE_KEY})


def charge(request):
    if request.method == 'POST':
        amount = request.POST['order_price']
        order_id = request.POST['order_id']
        try:
            charge = stripe.Charge.create(
                amount=int(amount) * 100,
                currency='rub',
                description='Оплата заказа',
                source=request.POST['stripeToken']
            )
            order = Order.objects.filter(pk=order_id).first()
            order.is_paid=True
            order.save()
            return render(request, 'flower_shop/result.html', context={'order': order})
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def bouquet_list_ajax(request):
    if 'event' in request.GET and 'price' in request.GET:
        price_range = request.GET['price']
        event_id = request.GET['event']
        page = request.GET.get('page')

        if price_range == "None":
            price_range = None
        else:
            price_range = tuple(map(int, price_range.split('-')))

        bouquets = Bouquet.objects.filter(occasion__id=event_id)

        if price_range is not None and len(price_range) == 2:
            bouquets = bouquets.filter(price__range=(price_range[0], price_range[1]))

        paginator = Paginator(bouquets, 6)
        bouquets = paginator.get_page(page)

        bouquets_serialized = serializers.serialize('json', bouquets)
    else:
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
