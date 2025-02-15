from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Products, ProductImage, SourcingProductRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import os
from django.conf import settings
from authentication.models import StaffUser
from fulfillX.access_control_decorater import role_required

# Create your views here.
@role_required('Staff')
@login_required(login_url='login')
@never_cache
def staff_dashboard(request):
    return render(request, 'staff/dashboard.html')

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def products(request):
    products = Products.objects.all()
    vendors = StaffUser.objects.filter(role='Vendor')
    return render(request, 'staff/products.html',{'products':products,
                                                  'vendors':vendors})

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def add_product(request):
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['price']
        description = request.POST['product_description']
        images = request.FILES.getlist('product_image')
        vendor = request.POST['vendor']
        category = request.POST['category']

        try:
            product = Products.objects.create(
                name=name,
                price=price,
                category=category,
                description=description,
                created_by=request.user.username,
                vendor = vendor
            )

            for img in images:
                product_image = ProductImage.objects.create(image=img)
                product.images.add(product_image)

            messages.success(request, 'Product added Successfully!')
            return redirect('staff_products')
        except:
            messages.error(request, 'Something went wrong. Please try again!')
            return redirect('staff_products')

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def update_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    vendors = StaffUser.objects.filter(role='Vendor')

    if request.method == "POST":
        # Update product details
        product.name = request.POST.get("name")
        product.price = request.POST.get('price')
        product.description = request.POST.get("description")
        product.inventory = request.POST.get("inventory")
        product.category = request.POST.get('category')
        product.save()

        # Delete selected images
        delete_image_ids = request.POST.getlist("delete_images")
        for image_id in delete_image_ids:
            try:
                image = ProductImage.objects.get(id=image_id)
                image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))

                # Delete the file from the file system if it exists
                if os.path.exists(image_path):
                    os.remove(image_path)

                # Delete the image object from the database
                image.delete()
            except ProductImage.DoesNotExist:
                pass

        # Add new images
        new_images = request.FILES.getlist("new_images")
        for image_file in new_images:
            product_image = ProductImage.objects.create(image=image_file)
            product.images.add(product_image)

        messages.success(request, "Product updated successfully!")
        return HttpResponseRedirect('/staff_products/#existing-products')

    return render(request, "staff/update_product.html", {"product": product,
                                                         'vendors':vendors})

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def delete_product(request, product_id):
    product = get_object_or_404(Products,id=product_id)
    
    for image in product.images.all():
        image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
        if os.path.exists(image_path):
            os.remove(image_path)  
        image.delete()  

    # Delete the product
    product.delete()

    messages.success(request, "Product and associated images deleted successfully.")
    return redirect('staff_products')

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def sourcing_requests(request):
    completed_requests = SourcingProductRequest.objects.filter(status='Completed')
    pending_requests = SourcingProductRequest.objects.filter(status='Pending')
    in_progress_requests = SourcingProductRequest.objects.filter(status='In Progress')
    rejected_requests = SourcingProductRequest.objects.filter(status='Rejected')
    return render(request, 'staff/sourcing_requests.html',{'completed_requests':completed_requests,
                                                           'pending_requests':pending_requests,
                                                           'in_progress_requests':in_progress_requests,
                                                           'rejected_requests':rejected_requests})

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def update_sourcing_req_status(request):
    if request.method == 'POST':
        id = request.POST['request_id']
        status = request.POST['status']
        review = request.POST['review']
        user = request.user.username

        try:
            req = get_object_or_404(SourcingProductRequest, id=id)
            req.status = status
            req.review = review
            req.updated_by = user
            req.save()

            messages.success(request, 'Status updated successfully!')
            return redirect('staff_sourcing_requests')
        except:
            messages.error(request, 'Please try again later!')
            return redirect('staff_sourcing_requests')