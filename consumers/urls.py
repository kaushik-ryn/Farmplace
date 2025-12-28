# from django.urls import path
# from . import views

# urlpatterns = [
#     path('search/', views.consumer_search, name='consumer_search'),
#     path('farmer/<int:farmer_id>/', views.farmer_crops, name='farmer_crops'),
#     path('dashboard/', views.consumer_dashboard, name='consumer_dashboard'),
#      path('order/bulk/', views.place_order_bulk, name='place_order_bulk'),
#      path("checkout/", views.checkout, name="checkout"),
#      path("orders/", views.consumer_orders, name="consumer_orders"),
#     #  path("orders/api/", views.consumer_orders_api, name="consumer_orders_api"),



# ]

from django.urls import path
from . import views

urlpatterns = [
     path('', views.consumer_home, name='consumer_home'),
    path('search/', views.consumer_search, name='consumer_search'),
    path('farmer/<int:farmer_id>/', views.farmer_crops, name='farmer_crops'),
    path('dashboard/', views.consumer_dashboard, name='consumer_dashboard'),
    path("checkout/", views.checkout, name="checkout"),
    path('orders/', views.my_orders, name='my_orders'),
    
]

