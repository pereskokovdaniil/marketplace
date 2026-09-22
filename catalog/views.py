from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product, Cart, CartItem, Category, Order, OrderItem
from .forms import ProductForm


def index(request):
    products = Product.objects.all()
    сategories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    search_query = request.GET.get('search_query')
    if search_query:
        products = products.filter(name__icontains=search_query)

    my_products = request.GET.get('my_products')
    if my_products and request.user.is_authenticated:
        products = products.filter(seller=request.user)

    return render(request, 'index.html', {
        'products': products,
        'categories': сategories
    })

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user != product.seller:
        return redirect('index')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_edit.html', {'form': form, 'product': product})

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
    total = 0
    for item in items:
        total += item.quantity * item.product.price

    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total': total})

def remove_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()

    return redirect('cart')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()

    for item in items:
        if item.product.stock < item.quantity:
            return redirect('cart')

    total = 0
    for item in items:
        total += item.quantity * item.product.price

    order = Order.objects.create(user=request.user, total=total)

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        item.product.stock -= item.quantity
        item.product.save()

    items.delete()

    return redirect('my_orders')


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_orders.html', {'orders': orders})
