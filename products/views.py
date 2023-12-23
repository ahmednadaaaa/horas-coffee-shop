from django.shortcuts import render, get_object_or_404
from .models import Product
# Create your views here.


def Product_list(request):
    product_list = Product.objects.all()
    context = {'product_list':product_list}
    return render(request, 'index.html', context)


def product_detail(request, pro_id):

    context = {
        'pro': get_object_or_404(Product, pk=pro_id)
    }
    return render(request, 'product_detail.html', context)


def menu(request):
    product_list = Product.objects.all()
    context = {'product_list':product_list}
    return render(request, 'menu.html', context)




