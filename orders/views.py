import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from farmers.models import Crop
from .models import Order, Notification, OrderItem
from farmers.models import FarmerProfile
from .models import Notification  
from django.contrib import messages


@login_required
def place_order_bulk(request):
    if request.method != "POST":
        return redirect("consumer_dashboard")

    cart_json = request.POST.get("cart_data")
    if not cart_json:
        return redirect("consumer_dashboard")

    cart = json.loads(cart_json)  # dict

    # 🔹 ASSUMPTION: all items belong to same farmer
    first_crop_id = list(cart.keys())[0]
    first_crop = Crop.objects.get(id=first_crop_id)
    farmer_profile = first_crop.farmer

    # ✅ CREATE ONE ORDER
    order = Order.objects.create(
        consumer=request.user,
        farmer=farmer_profile,
        status="pending"
    )

    # ✅ CREATE MULTIPLE ORDER ITEMS
    for crop_id, item in cart.items():
        crop = Crop.objects.get(id=crop_id)

        OrderItem.objects.create(
            order=order,
            crop=crop,
            quantity=item["qty"],
            price_per_kg=crop.price_per_kg
        )

    # 🔔 SINGLE NOTIFICATION TO FARMER
    Notification.objects.create(
        user=farmer_profile.user,
        order=order,
        message=f"New bulk order received from {request.user.username}"
    )

    request.session["cart"] = {}

    # ✅ RENDER CHECKOUT WITH SUCCESS FLAG
    return render(
        request,
        "consumers/checkout.html",
        {
            "order_success": True
        }
    )





# @login_required
# def place_order_bulk(request):
#     if request.method != "POST":
#         return redirect("consumer_search")

#     cart_data = request.POST.get("cart_data")

#     # 🛑 Empty cart protection
#     if not cart_data:
#         return redirect("consumer_search")

#     # 🔐 JSON → Python dict
#     try:
#         cart = json.loads(cart_data)
#     except json.JSONDecodeError:
#         return redirect("consumer_search")

#     # ✅ Loop correctly
#     for crop_id, item in cart.items():
#         crop = Crop.objects.get(id=crop_id)
#         farmer = crop.farmer

#         quantity = int(item["qty"])

#         # 🛑 Stock safety
#         if quantity > crop.quantity:
#             continue

#         # ✅ Create order
#         Order.objects.create(
#             consumer=request.user,
#             farmer=farmer,
#             crop=crop,
#             quantity=quantity,
#             price=crop.price_per_kg,
#             status="pending"
#         )

#         # 🔄 Reduce stock
#         crop.quantity -= quantity
#         crop.save()

#     return redirect("consumer_orders")


@login_required
def consumer_orders(request):
    orders = (
        Order.objects
        .filter(consumer=request.user)
        .prefetch_related("items__crop")
        .order_by("-created_at")
    )

    # Calculate totals
    for order in orders:
        order.total_price = 0  # total for this order
        for item in order.items.all():
            item.subtotal = item.quantity * item.price_per_kg
            order.total_price += item.subtotal
    
    return render(request, "consumers/my_orders.html", {
        "orders": orders,
    })



@login_required
def farmer_orders(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)

    orders = Order.objects.filter(
        farmer=farmer
    ).select_related("crop", "consumer").order_by("-created_at")

    return render(request, "orders/farmer_orders.html", {
        "orders": orders
    })


# @login_required
# def update_order_status(request, order_id, status):
#     order = get_object_or_404(Order, id=order_id)

#     # security check
#     if order.farmer.user != request.user:
#         return redirect('farmer_dashboard')

#     if status in ['accepted', 'cancelled']:
#         order.status = status
#         order.save()

#         # 🔔 NOTIFY CONSUMER
#         Notification.objects.create(
#             user=order.consumer,
#             order=order,
#             message=f"Your order for {order.crop.name} ({order.quantity} kg) was {status}"
#         )

#     return redirect('farmer_dashboard')
# @login_required
# def update_order_status(request, order_id, status):
#     order = get_object_or_404(Order, id=order_id)

#     # security check
#     if order.farmer.user != request.user:
#         return redirect('farmer_orders')

#     if status == 'accepted':
#         # ✅ Check stock first
#         if order.crop.quantity >= order.quantity:
#             order.status = 'accepted'
#             order.crop.quantity -= order.quantity  # 🔥 STOCK DEDUCTED HERE
#             order.crop.save()
#             order.save()

#             # 🔔 Notify consumer
#             Notification.objects.create(
#                 user=order.consumer,
#                 message=f"Your order for {order.crop.name} has been ACCEPTED"
#             )
#         else:
#             # Optional safety
#             order.status = 'rejected'
#             order.save()

#     elif status == 'rejected':
#         order.status = 'rejected'
#         order.save()

#         # 🔔 Notify consumer
#         Notification.objects.create(
#             user=order.consumer,
#             message=f"Your order for {order.crop.name} has been REJECTED"
#         )

#     return redirect('farmer_orders')


@login_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(
        Order,
        id=order_id,
        farmer__user=request.user
    )

    # ❌ Prevent double-processing
    if order.status != "pending":
        messages.warning(request, "Order already processed.")
        return redirect("farmer_dashboard")

    if status == "accepted":
        # ✅ Deduct stock
        for item in order.items.select_related("crop"):
            crop = item.crop

            if crop.quantity < item.quantity:
                messages.error(
                    request,
                    f"Not enough stock for {crop.name}"
                )
                return redirect("farmer_dashboard")

            crop.quantity -= item.quantity
            crop.save()

        order.status = "accepted"
        order.save()

        # 🔔 Notify consumer
        Notification.objects.create(
            user=order.consumer,
            order=order,
            message=f"Order #{order.id} has been accepted 🎉"
        )

        messages.success(request, "Order accepted successfully.")

    elif status == "cancelled":
        order.status = "cancelled"
        order.save()

        Notification.objects.create(
            user=order.consumer,
            order=order,
            message=f"Order #{order.id} was rejected ❌"
        )

        messages.info(request, "Order rejected.")

    return redirect("farmer_dashboard")


@login_required
def farmer_order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        farmer__user=request.user
    )

    items = order.items.select_related("crop")

    # ✅ calculate totals in backend
    grand_total = 0
    for item in items:
        item.subtotal = item.quantity * item.price_per_kg
        grand_total += item.subtotal

    return render(request, "orders/farmer_order_detail.html", {
        "order": order,
        "items": items,
        "grand_total": grand_total
    })


@login_required
def pay_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        consumer=request.user,
        status="accepted"
    )

    # Simulate payment success
    order.payment_done = True
    order.status = "paid"
    order.save()

    # 🔔 Notify farmer
    Notification.objects.create(
        user=order.farmer.user,
        order=order,
        message=f"Payment received for Order #{order.id}"
    )

    messages.success(request, "Payment successful! Your order is confirmed.")
    return redirect("consumer_orders")
