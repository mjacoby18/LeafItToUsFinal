from django.shortcuts import render, get_object_or_404
from .models import Category, Product  # Import Category and Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from orders.models import Order  # Import Order from orders.models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test  # Import for admin check
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView



@user_passes_test(lambda u: u.is_superuser)  # Ensure only superusers can access this page
def admin_page(request):
    products = Product.objects.all()  # Fetch all products for display
    return render(request, 'shop/admin.html', {'products': products})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart = Cart(request)
    return render(request,
                  'shop/product/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'cart': cart})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    # Set choices for quantity available based on inventory and items in this session's cart
    cart = Cart(request)
    cartquantity = 0
    # If item in cart, subtract the items in the cart from the quantity available
    for item in cart:
        cartproduct = get_object_or_404(Product, id=item['product'].id)
        if product == cartproduct:
            cartquantity = item['quantity']
            break
    if product.quantity - cartquantity > 0:
        choices = [(i, str(i)) for i in range(1, product.quantity - cartquantity + 1)]
    else:  # No items left in inventory for this session
        choices = [(1, 0)]

    cart_product_form = CartAddProductForm(my_choices=choices)
    return render(request,
                  'shop/product/product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'cart': cart})

# View for showing all orders for a logged-in user
def order_history_view(request):
    if request.user.is_authenticated:  # Check if user is authenticated
        orders = Order.objects.filter(user=request.user)  # Use user instead of customer
    else:
        orders = []  # Return an empty list if not authenticated
    return render(request, 'shop/order_history.html', {'orders': orders})

# View for showing details of a specific order
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)  # Ensure to use user
    return render(request, 'shop/order_detail.html', {'order': order})

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'category', 'image', 'price', 'quantity']
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('shop:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'category', 'image', 'price', 'quantity']
    template_name = 'shop/product_edit.html'
    success_url = reverse_lazy('shop:admin_page')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_delete.html'
    success_url = reverse_lazy('shop:admin_page')