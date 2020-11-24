from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.http import JsonResponse
import json


def store(request):
    order = Order()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)

    else:
        items = json.loads(request.COOKIES.get("cart"))
        newitems = []
        order = {}

        for item in items:
            newitem = {}
            product = Product.objects.get(id=item["productId"])
            newitem["product"] = product
            newitem["quantity"] = item["quantity"]
            newitem["calculate_total"] = newitem["quantity"]*product.Price
            newitems.append(newitem)

        items = newitems
        total = 0
        total_price = 0
        for orderitem in items:
            total += orderitem["quantity"]
            total_price += orderitem["calculate_total"]
        order["total_order_price"] = total_price
        order["total_quantity"] = total
    products = Product.objects.all()
    context = {"products": products, "order": order}
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)
        items = order.get_all_order_items

    else:
        items = json.loads(request.COOKIES.get("cart"))
        newitems = []
        order = {}

        for item in items:
            newitem = {}
            product = Product.objects.get(id=item["productId"])
            newitem["product"] = product
            newitem["quantity"] = item["quantity"]
            newitem["calculate_total"] = newitem["quantity"]*product.Price
            newitems.append(newitem)

        items = newitems
        total = 0
        total_price = 0
        for orderitem in items:
            total += orderitem["quantity"]
            total_price += orderitem["calculate_total"]
        order["total_order_price"] = total_price
        order["total_quantity"] = total

    context = {"items": items, "order": order}
    return render(request, "store/cart.html", context)


def checkout(request):
    order = Order()
    shipping = False
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)
        items = order.get_all_order_items

        for item in items:
            if item.product.digital == False:
                shipping = True

    else:
        items = json.loads(request.COOKIES.get("cart"))
        newitems = []
        order = {}

        for item in items:
            newitem = {}
            product = Product.objects.get(id=item["productId"])
            newitem["product"] = product
            newitem["quantity"] = item["quantity"]
            newitem["calculate_total"] = newitem["quantity"]*product.Price
            newitems.append(newitem)

        items = newitems
        total = 0
        total_price = 0

        for item in items:
            if item["product"].digital == False:
                shipping = True

        for orderitem in items:
            total += orderitem["quantity"]
            total_price += orderitem["calculate_total"]
        order["total_order_price"] = total_price
        order["total_quantity"] = total
    context = {"items": items, "order": order, "shipping": shipping}
    return render(request, "store/checkout.html", context)


def update_order_item(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        product = Product.objects.get(id=data["product_id"])
        orderitem, created = OrderItem.objects.get_or_create(
            order=order, product=product)
        print(data)
        if data["action"] == "add":
            print(orderitem.quantity)
            orderitem.quantity += 1
            orderitem.save()
        elif orderitem.quantity == 1 and data["action"] == "remove":
            orderitem.delete()
        elif data["action"] == "remove":
            orderitem.quantity -= 1
            orderitem.save()

    return JsonResponse({"data": data}, safe=False)
