from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from staff.models import Products, SourcingProductRequest
from django.contrib import messages
from fulfillX.access_control_decorater import role_required
import shopify
from django.conf import settings
from django.http import HttpResponse
import urllib.parse
import requests
from .models import Shop

# Create your views here.
@role_required('User')
@login_required(login_url='login')
@never_cache
def usr_dashboard(request):
    return render(request, 'user/dashboard.html')

@role_required('User')
@login_required(login_url='login')
@never_cache
def custom_products(request):
    return render(request, 'user/custom_products.html')

@role_required('User')
@login_required(login_url='login')
@never_cache
def find_products(request):
    products = Products.objects.all()
    return render(request, 'user/find_products.html',{'products':products})

@role_required('User')
@login_required(login_url='login')
@never_cache
def import_list(request):
    return render(request, 'user/import_list.html')

@role_required('User')
@login_required(login_url='login')
@never_cache
def manage_store(request):
    user = request.user.username
    #shops = Shop.objects.filter(linked_by=user)
    shops = Shop.objects.all()
    return render(request, 'user/manage_store.html',{'shops':shops})

@role_required('User')
@login_required(login_url='login')
@never_cache
def my_products(request):
    return render(request, 'user/my_products.html')

@role_required('User')
@login_required(login_url='login')
@never_cache
def sourcing(request):
    username = request.user.username
    sourcing_requests = SourcingProductRequest.objects.filter(added_by=username)
    return render(request, 'user/sourcing.html',{'sourcing_requests':sourcing_requests})

@role_required('User')
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

@role_required('User')
@login_required(login_url='login')
@never_cache
def shopify_callback(request):
    # Ensure the request is a GET request
    if request.method != 'GET':
        return HttpResponse("Invalid request method. Expected GET.", status=400)
    
    # Retrieve the 'shop' and 'code' parameters from the GET request
    shop = request.GET.get('shop')
    code = request.GET.get('code')

    # Validate that 'shop' and 'code' are present
    if not shop or not code:
        return HttpResponse("Missing 'shop' or 'code' parameters.", status=400)

    # Exchange the code for an access token
    url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": settings.SHOPIFY_API_KEY,
        "client_secret": settings.SHOPIFY_API_SECRET,
        "code": code,
    }

    # Send POST request to exchange the code for an access token
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        shop_info_url = f"https://{shop}/admin/api/2023-01/shop.json"
        headers = {"X-Shopify-Access-Token": access_token}
        shop_response = requests.get(shop_info_url, headers=headers)

        if shop_response.status_code == 200:
                shop_data = shop_response.json().get('shop', {})
                shop_name = shop_data.get('name', 'Unknown Shop')

        Shop.objects.create(
            shop_name=shop_name,
            shop_url=shop,
            access_token=access_token,
            shop_platform="Shopify",
            linked_by=request.user.username
        )
        return redirect('usr_dashboard')  # Redirect to your dashboard or desired page
    else:
        return HttpResponse(f"Failed to get access token: {response.text}", status=400)
    
def shopify_auth(request):
    shopify_api_key = settings.SHOPIFY_API_KEY
    redirect_uri = settings.SHOPIFY_REDIRECT_URI
    scopes = "read_products,write_products"  # Adjust scopes based on your app's requirements
    if request.method == 'POST':
        shop = request.POST['shop']
        if not shop:
            return HttpResponse("Missing 'shop' parameter.", status=400)

    # Construct the OAuth URL
    oauth_url = f"https://{shop}/admin/oauth/authorize"
    params = {
        "client_id": shopify_api_key,
        "scope": scopes,
        "redirect_uri": redirect_uri,
    }
    full_url = f"{oauth_url}?{urllib.parse.urlencode(params)}"

    return redirect(full_url)