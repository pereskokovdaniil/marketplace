from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product, Cart, CartItem
from .forms import ProductForm


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_product(request):
    if request.user.profile.role != 'seller':
        return redirect('index')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def add_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('index')

def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart.html', {'cart': cart, 'items': items})

def remove_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()

    return redirect('cart')
