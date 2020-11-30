import json
from .models import Product, Order, ShippingAddress


def cookiesCart(request):
    shipping = False
    items = []
    order = {}
    order["total_quantity"] = 0
    try:
        items = json.loads(request.COOKIES.get("cart"))
        newitems = []
        if len(items) != 0:
            for item in items:
                try:
                    newitem = {}
                    print(item["productId"])
                    product = Product.objects.get(id=item["productId"])
                    newitem["product"] = product
                    newitem["quantity"] = item["quantity"]
                    newitem["calculate_total"] = newitem["quantity"] * \
                        product.Price
                    newitems.append(newitem)

                    items = newitems
                    for item in items:
                        if item["product"].digital == False:
                            shipping = True
                    total = 0
                    total_price = 0
                    for orderitem in items:
                        total += orderitem["quantity"]
                        total_price += orderitem["calculate_total"]
                    order["total_order_price"] = total_price
                    order["total_quantity"] = total

                except:
                    pass
    except:
        pass

    return {"order": order, "items": items, "shipping": shipping}


def authenticatedData(request):
    shipping = False
    order, created = Order.objects.get_or_create(
        customer=request.user.customer, complete=False)
    items = order.get_all_order_items

    for item in items:
        if item.product.digital == False:
            shipping = True

    return {"order": order, "items": items, "shipping": shipping}


def contextData(request):
    if request.user.is_authenticated:
        return authenticatedData(request)
    else:
        return cookiesCart(request)


# def shippingAddressOption(request, shippingOptions):
#     if request.user.is_authenticated:

#     else:
#         data = cookiesCart()
