from django.shortcuts import render, get_object_or_404

from flower_shop.models import Bouquet


def view_bouquet(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)

    return render(request, 'flower_shop/card.html', context={'bouquet': bouquet})
