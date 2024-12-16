from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, 
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('product/create/', views.ProductCreateView.as_view(),
         name='product_create'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(),
         name='product_delete'),
    path('product/edit/<int:pk>/', views.ProductUpdateView.as_view(),
         name='product_edit'),
    path('admin-products/', views.admin_page, name='admin_page'),
]