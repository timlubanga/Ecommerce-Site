from django.shortcuts import render
from store.models import Product, Order, OrderItem, ShippingAddress, Customer
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect
import json
import uuid
from store.utils import cookiesCart, contextData, authenticatedData


def store(request):
    products = Product.objects.all()
    print(products)
    contextInfo = contextData(request)
    order = contextInfo["order"]
    context = {"order": order}
    return render(request, "store/store.html", context)


def cart(request):
    contextInfo = contextData(request)
    order = contextInfo["order"]
    items = contextInfo["items"]
    context = {"items": items, "order": order}
    return render(request, "store/cart.html", context)


def checkout(request):
    contextInfo = contextData(request)
    order = contextInfo["order"]
    items = contextInfo["items"]
    shipping = contextInfo["shipping"]
    context = {"items": items, "order": order, "shipping": shipping}
    return render(request, "store/checkout.html", context)


def update_order_item(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        order.save()
        product = Product.objects.get(id=data["product_id"])
        orderitem, created = OrderItem.objects.get_or_create(
            order=order, product=product)
        if data["action"] == "add":
            orderitem.quantity += 1
            orderitem.save()
        elif orderitem.quantity == 1 and data["action"] == "remove":
            orderitem.delete()
        elif data["action"] == "remove":
            orderitem.quantity -= 1
            orderitem.save()

    return JsonResponse({"data": "order updated"}, safe=False)


def processOrder(request):
    transaction_id = uuid.uuid4()
    if request.user.is_authenticated:
        data = authenticatedData(request)
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)
        order.transaction_id = transaction_id
        if data["shipping"]:
            customerDetails = json.loads(request.body)
            shippingaddress, created = ShippingAddress.objects.get_or_create(
                customer=request.user.customer)
            shippingaddress.order = data["order"]
            shippingaddress.zipcode = customerDetails["shippingInfo"]["zipCode"]
            shippingaddress.address = customerDetails["shippingInfo"]["address"]
            shippingaddress.city = customerDetails["shippingInfo"]["city"]
            shippingaddress.state = customerDetails["shippingInfo"]["state"]
            shippingaddress.save()
            order.complete = True
            order.save()

        return JsonResponse({"data": "order updated"}, safe=False)

    else:
        data = cookiesCart(request)
        customerDetails = json.loads(request.body)
        customerName = customerDetails["userSubmitData"]["name"]
        customerEmail = customerDetails["userSubmitData"]["email"]
        customer, created = Customer.objects.get_or_create(email=customerEmail)
        customer.name = customerName
        customer.save()
        order = Order.objects.create(
            complete=False, customer=customer, transaction_id=transaction_id)

        if data["shipping"]:
            shippingaddress, created = ShippingAddress.objects.get_or_create(
                customer=customer)

            shippingaddress.order = order
            shippingaddress.zipcode = customerDetails["shippingInfo"]["zipCode"]
            shippingaddress.address = customerDetails["shippingInfo"]["address"]
            shippingaddress.city = customerDetails["shippingInfo"]["city"]
            shippingaddress.state = customerDetails["shippingInfo"]["state"]
            shippingaddress.save()

        for item in data["items"]:
            OrderItem.objects.create(
                product=item["product"], order=order, quantity=item["quantity"])
            order.complete = True
            order.save()
        return JsonResponse({"data": "order  transaction complete"}, safe=False)
