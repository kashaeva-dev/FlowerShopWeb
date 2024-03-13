from django.shortcuts import render, get_object_or_404
from flower_shop.models import Bouquet


def view_bouquet(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    return render(request, 'flower_shop/card.html', context={'bouquet': bouquet})


def index(request):
    recommended_bouquets = Bouquet.objects.filter(is_recommended=True)[:3]
    return render(request, 'flower_shop/index.html', context={'recommended_bouquets': recommended_bouquets})


def show_catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'flower_shop/catalog.html', context={'bouquets': bouquets})
