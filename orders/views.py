from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import Order, OrderDetail
from django.utils import timezone
# Create your views here.


def add_to_cart(request):

    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous :

        pro_id = request.GET['pro_id']
        qty = request.GET['qty']

        order = Order.objects.all().filter(user=request.user, is_finished=False)

        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products')
        pro = Product.objects.get(id=pro_id)

        if order:
            messages.success(request,'يوجد طلب قديم')
            old_order = Order.objects.get(user=request.user.id, is_finished=False)
            if OrderDetail.objects.all().filter(order=old_order, product=pro).exists():
                orderdetails = OrderDetail.objects.get(order=old_order, product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else :
                orderdetails = OrderDetail.objects.create(product=pro,
                order=old_order, price=pro.price, quantity=qty)
            messages.success(request, 'was added to cart for old order')
        else :
            messages.success(request,'هنا سوف يتم عمل طلب')
            new_order = Order()
            new_order.user =request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            oderdetails = OrderDetail.objects.create(product=pro, order=new_order, price=pro.price, quantity=qty)
            messages.success(request, 'was added to cart for new order')

        return redirect('/products/' + request.GET['pro_id'])

    else:

      return redirect('products')


def cart(request):
    context = None
    if Order.objects.all().filter(user=request.user.id, is_finished=False):
        order = Order.objects.get(user=request.user.id, is_finished=False)
        orderdetails = OrderDetail.objects.all().filter(order=order)
        total = 0
        for sub in orderdetails:
            total +=sub.price * sub.quantity

        context = {
            'order':order,
            'orderdetails':orderdetails,
            'total':total,

        }

    return render(request, 'order/cart.html', context)


def remove_from_cart(request, orderdetails_id):
   if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderDetail.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id==request.user.id:
     orderdetails.delete()
    return redirect('cart')


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetail.objects.get(id=orderdetails_id)
        orderdetails.quantity +=1
        orderdetails.save()

    return redirect('cart')


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetail.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
            orderdetails.save()

    return redirect('cart')




def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.get(id=x.id)
                orderdetails = OrderDetail.objects.all().filter(order=order)
                total = 0
                for sub in orderdetails:
                    total +=sub.price * sub.quantity
                    x.total = total
                    x.items_count = orderdetails.count
    context = {'all_orders':all_orders}
    return render(request, 'order/show_orders.html', context)



