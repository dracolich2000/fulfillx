from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from staff.models import Products, SourcingProductRequest
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
@never_cache
def usr_dashboard(request):
    return render(request, 'user/dashboard.html')

@login_required(login_url='login')
@never_cache
def custom_products(request):
    return render(request, 'user/custom_products.html')

@login_required(login_url='login')
@never_cache
def find_products(request):
    products = Products.objects.all()
    return render(request, 'user/find_products.html',{'products':products})

@login_required(login_url='login')
@never_cache
def import_list(request):
    return render(request, 'user/import_list.html')

@login_required(login_url='login')
@never_cache
def manage_store(request):
    return render(request, 'user/manage_store.html')

@login_required(login_url='login')
@never_cache
def my_products(request):
    return render(request, 'user/my_products.html')

@login_required(login_url='login')
@never_cache
def sourcing(request):
    username = request.user.username
    sourcing_requests = SourcingProductRequest.objects.filter(added_by=username)
    return render(request, 'user/sourcing.html',{'sourcing_requests':sourcing_requests})

@login_required(login_url='login')
@never_cache
def new_sourcing_request(request):
    if request.method == 'POST':
        name = request.POST['product_name']
        link = request.POST['product_link']
        image = request.FILES.get('product_image')
        description = request.POST['description']
        username = request.user.username

        try:
            sourcing_product_request = SourcingProductRequest.objects.create(
                name=name,
                link=link,
                image=image,
                description=description,
                added_by = username
            )
            messages.success(request, 'Request submitted! Please check request status for updates.')
            return redirect('user_sourcing')
        except:
            messages.error(request, 'Please try again after some time!')
            return redirect('user_sourcing')

