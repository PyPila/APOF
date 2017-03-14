from django.shortcuts import render


def basket_view(request):
    return render(request, 'baskets/basket.html')
