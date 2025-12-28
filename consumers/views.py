from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ConsumerProfile
from farmers.models import FarmerProfile, Crop
import json
from orders.models import Order
# from .models import Order
# from django.http import JsonResponse 


from django.db.models import Q
@login_required
def consumer_search(request):
    farmers = FarmerProfile.objects.none()
    searched = False

    location = request.GET.get("location") or request.POST.get("location")
    crop = request.GET.get("crop") or request.POST.get("crop")

    if location:
        searched = True

        farmers = FarmerProfile.objects.filter(
            location__icontains=location
        )

        # optional crop filter
        if crop:
            farmers = farmers.filter(
                crops__name__icontains=crop
            ).distinct()

    return render(request, "consumers/search.html", {
        "farmers": farmers,
        "searched": searched,
        "searched_location": location,
        "searched_crop": crop
    })


@login_required
def farmer_crops(request, farmer_id):
    farmer = FarmerProfile.objects.get(id=farmer_id)
    crops = Crop.objects.filter(farmer=farmer)
    return render(request, 'consumers/farmer_crops.html', {'farmer': farmer, 'crops': crops})

@login_required
def consumer_notifications(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'consumers/notifications.html', {
        'notifications': notifications
    })

@login_required
def consumer_dashboard(request):
    crops = Crop.objects.filter(quantity__gt=0)
    return render(request, 'consumers/search.html', {'crops': crops})

@login_required
def checkout(request):
    cart_data = request.POST.get("cart_data")

    # Safety check
    if not cart_data:
        return redirect("consumer_dashboard")

    cart = json.loads(cart_data)

    cart_items = []
    total_price = 0

    for crop_id, item in cart.items():
        crop = Crop.objects.get(id=crop_id)
        qty = item["qty"]
        subtotal = crop.price_per_kg * qty

        cart_items.append({
            "crop": crop,
            "quantity": qty,
            "subtotal": subtotal
        })

        total_price += subtotal

    return render(request, "consumers/checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "cart_data": cart_data   # 🔥 PASS THIS
    })


# @login_required
# def checkout(request):
#     if request.method == "POST":

#         cart_data = request.POST.get("cart_data")

#         # 🔐 Step 1: Empty cart protection
#         if not cart_data:
#             return redirect("consumer_search")

#         # 🔐 Step 2: Convert JSON string → Python dict
#         try:
#             cart = json.loads(cart_data)
#         except json.JSONDecodeError:
#             return redirect("consumer_search")

#         cart_items = []
#         total_price = 0

#         # 🔐 Step 3: Loop properly
#         for crop_id, item in cart.items():
#             crop = Crop.objects.get(id=crop_id)

#             quantity = int(item["qty"])
#             subtotal = quantity * crop.price_per_kg
#             total_price += subtotal

#             cart_items.append({
#                 "crop": crop,
#                 "quantity": quantity,
#                 "subtotal": subtotal
#             })

#         return render(request, "consumers/checkout.html", {
#             "cart_items": cart_items,
#             "total_price": total_price
#         })

#     return redirect("consumer_search")


# @login_required
# def consumer_orders_api(request):
#     orders = Order.objects.filter(consumer=request.user).order_by('-created_at')

#     data = []
#     for order in orders:
#         data.append({
#             "crop": order.crop.name,
#             "quantity": order.quantity,
#             "status": order.status,
#             "phone": order.farmer.phone if order.status == "accepted" else None
#         })

#     return JsonResponse({"orders": data})
def consumer_home(request):
    return render(request, 'consumers/search.html')  # same page as search/home

def my_orders(request):
    orders = Order.objects.filter(
        consumer=request.user
    ).prefetch_related("items__crop").order_by("-created_at")
    grand_total = sum(order.total_price for order in orders)

    return render(request, "consumers/my_orders.html", {
        "orders": orders,
        "grand_total": grand_total
    })
