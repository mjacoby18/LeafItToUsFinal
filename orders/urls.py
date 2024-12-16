from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),  # For creating a new order
    path('created/', views.order_created, name='order_created'),  # For confirming order creation
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),  # Admin order detail
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),  # Order detail for users
    path('history/', views.order_history_view, name='order_history'),  # User order history
]