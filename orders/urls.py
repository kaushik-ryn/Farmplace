# from django.urls import path
# from . import views

# urlpatterns = [
#     path('consumer/', views.consumer_orders, name='consumer_orders'),
#     path('farmer/', views.farmer_orders, name='farmer_orders'),
#     path('orders/', views.consumer_orders, name='consumer_orders'),
#     path('place-order/', views.place_order_bulk, name='place_order_bulk'),
#     path(
#         'update/<int:order_id>/<str:status>/',
#         views.update_order_status,
#         name='update_order_status'
#     ),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path("place/", views.place_order_bulk, name="place_order_bulk"),
    path("my-orders/", views.consumer_orders, name="consumer_orders"),
    path("farmer-orders/", views.farmer_orders, name="farmer_orders"),
path(
    "order/<int:order_id>/<str:status>/",
    views.update_order_status,
    name="update_order_status"
),

    # orders/urls.py
path(
    "farmer/order/<int:order_id>/",
    views.farmer_order_detail,
    name="farmer_order_detail"
),


]
