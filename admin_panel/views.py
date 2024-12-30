from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import StaffUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from staff.models import Products


# Create your views here.
@login_required(login_url='login')
@never_cache
def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

@login_required(login_url='login')
@never_cache
def users(request):
    staff_users = StaffUser.objects.filter(role='Staff')
    vendor_users = StaffUser.objects.filter(role='Vendor')
    regular_users = StaffUser.objects.filter(role='User')
    return render(request, 'admin_panel/users.html',{'staff':staff_users,
                                                     'vendors':vendor_users,
                                                     'users': regular_users})

@login_required(login_url='login')
@never_cache
def user_details(request, user_id):
    user = get_object_or_404(StaffUser, id=user_id)
    return render(request, 'admin_panel/user_details.html', {'user':user})


@login_required(login_url='login')
@never_cache
def assign_role(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role = request.POST.get("role")

        try:
            user = get_object_or_404(StaffUser, id=user_id)
            user.role = role

            if role == "User":
                user.is_staff = False
                user.is_superuser = False
            elif role == "Vendor":
                user.is_staff = False
                user.is_superuser = False
            elif role == "Staff":
                user.is_staff = True
                user.is_superuser = False
            else:
                messages.error(request, "Invalid role selected.")
                return redirect('users')  # Redirect to the users page
            
            user.save()

            # Add success message
            messages.success(request, f"Role for user {user.username} updated to {role}.")
        except StaffUser.DoesNotExist:
            messages.error(request, "User not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('users')  # Redirect to the users page after assigning role

    # Redirect if request is not POST
    messages.error(request, "Invalid request method.")
    return redirect('users')

@login_required(login_url='login')
@never_cache
def products(request):
    products = Products.objects.all()
    return render(request, 'admin_panel/products.html',{'products':products})