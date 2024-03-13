from django.shortcuts import render


def index(request):
    return render(request, 'flower_shop/index.html')
