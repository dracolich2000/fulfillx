from django.shortcuts import render, redirect, get_object_or_404
from staff.models import Products
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@login_required(login_url='login')
@never_cache
def vendor_dashboard(request):
    return render(request, 'vendor/dashboard.html')

@login_required(login_url='login')
@never_cache
def products(request):
    vendor = request.user.username
    products = Products.objects.filter(vendor=vendor)
    return render(request, 'vendor/products.html',{'products':products})

@login_required(login_url='login')
@never_cache
def update_inventory(request):
    try:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            print(product_id)
            inventory = request.POST.get('inventory')
            product = get_object_or_404(Products, id=product_id)
            product.inventory = inventory
            product.save()
            
            messages.success(request, 'Inventory updated successfully!')
            return redirect('vendor_products')
    except:
        messages.error(request, 'Please try again!')
        return redirect('vendor_products')
