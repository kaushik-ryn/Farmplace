from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('add-crop/', views.add_crop, name='add_crop'),
    path('update-location/', views.update_location, name='update_location'),
    path('edit-crop/<int:crop_id>/', views.edit_crop, name='edit_crop'),
    path('delete-crop/<int:crop_id>/', views.delete_crop, name='delete_crop'),
    
]
