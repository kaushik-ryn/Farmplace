from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FarmerProfile, Crop
from orders.models import Notification



# @login_required
# def farmer_dashboard(request):
#     crops = Crop.objects.filter(farmer=request.user)

#     notifications = request.user.notifications.filter(
#         is_read=False
#     ).order_by('-created_at')

#     return render(request, 'farmers/dashboard.html', {
#         'crops': crops,
#         'notifications': notifications
#     })
# @login_required
# def farmer_dashboard(request):
#     farmer_profile = FarmerProfile.objects.get(user=request.user)

#     crops = Crop.objects.filter(farmer=farmer_profile)

#     notifications = request.user.notifications.filter(
#         is_read=False
#     ).order_by('-created_at')

#     return render(request, 'farmers/dashboard.html', {
#         'crops': crops,
#         'notifications': notifications
#     })
@login_required
def farmer_dashboard(request):
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        # 👇 SAFE fallback instead of error
        return render(request, 'farmers/dashboard.html', {
            'crops': [],
            'notifications': [],
            'error': 'Farmer profile not found'
        })

    crops = Crop.objects.filter(farmer=farmer_profile)
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'farmers/dashboard.html', {
        'crops': crops,
        'notifications': notifications
    })

@login_required
def add_crop(request):
    farmer = FarmerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']

        Crop.objects.create(
            farmer=farmer,
            name=name,
            price_per_kg=price,
            quantity=quantity
        )
        return redirect('farmer_dashboard')

    return render(request, 'farmers/add_crop.html')

@login_required
def update_location(request):
    farmer = FarmerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        farmer.location = request.POST.get('location')
        farmer.phone = request.POST.get('phone')
        farmer.save()
        return redirect('farmer_dashboard')

    return render(request, 'farmers/update_location.html', {'farmer': farmer})

@login_required
def farmer_dashboard(request):
    farmer = FarmerProfile.objects.get(user=request.user)

    crops = Crop.objects.filter(farmer=farmer)
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by("-created_at")

    return render(request, "farmers/dashboard.html", {
        "crops": crops,
        "notifications": notifications
    })

# @login_required
# def edit_crop(request, crop_id):
#     crop = get_object_or_404(Crop, id=crop_id, farmer__user=request.user)

#     if request.method == "POST":
#         name = request.POST.get("name")
#         price = request.POST.get("price")
#         quantity = request.POST.get("quantity")

#         crop.name = name
#         crop.price_per_kg = price
#         crop.quantity = quantity
#         crop.save()

#         return redirect('farmer_dashboard')

#     return render(request, "farmers/edit_crop.html", {"crop": crop})
@login_required
def edit_crop(request, crop_id):
    farmer = get_object_or_404(FarmerProfile, user=request.user)

    crop = get_object_or_404(Crop, id=crop_id, farmer=farmer)

    if request.method == "POST":
        crop.name = request.POST.get("name")
        crop.price_per_kg = request.POST.get("price")
        crop.quantity = request.POST.get("quantity")
        crop.save()

        return redirect("farmer_dashboard")

    return render(request, "farmers/edit_crop.html", {"crop": crop})

@login_required
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer__user=request.user)
    crop.delete()
    return redirect('farmer_dashboard')

# @login_required
# def farmer_order_detail(request, order_id):
#     order = get_object_or_404(
#         Order,
#         id=order_id,
#         farmer__user=request.user
#     )
#     return render(request, "farmers/order_detail.html", {"order": order})
