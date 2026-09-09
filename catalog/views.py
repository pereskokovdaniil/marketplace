from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from catalog.models import Product
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
