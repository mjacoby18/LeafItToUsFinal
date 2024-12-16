from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Assign the current user to the order
            order.save()

            for item in cart:
                product = item['product']
                quantity = item['quantity']

                # Check for sufficient stock
                if product.quantity < quantity:
                    return render(request, 'orders/create.html', {
                        'cart': cart,
                        'form': form,
                        'error': f'Not enough stock for {product.name}.'
                    })

                OrderItem.objects.create(order=order,
                                         product=product,
                                         price=item['price'],
                                         quantity=quantity)
                product.quantity -= quantity
                product.save()

            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:order_created')  # Redirect to the order_created view

    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@login_required
def order_created(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)  # Get the order to display confirmation
    return render(request, 'orders/created.html', {'order_id': order_id, 'order': order})

@login_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)  # Ensure only the user can view their order
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user)  # Fetch orders specific to the logged-in user
    return render(request, 'orders/order_history.html', {'orders': orders})