from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard',views.usr_dashboard,name='usr_dashboard'),
    path('custom_products',views.custom_products,name='custom_products'),
    path('find_products',views.find_products,name='find_products'),
    path('import_list',views.import_list,name='import_list'),
    path('manage_store',views.manage_store,name='manage_store'),
    path('my_products',views.my_products,name='my_products'),
    path('sourcing/',views.sourcing,name='user_sourcing'),
    path('new_sourcing_request',views.new_sourcing_request,name='new_sourcing_request')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)