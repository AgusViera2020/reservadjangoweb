from django.contrib import admin
from django.urls import include, path
from . import views
from django.views.generic.base import TemplateView  # new
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

app_name = 'payment'

urlpatterns = [
    path("payment_success/", views.payment_success, name = "payment_success"),
    path("billing_info/", views.billing_info, name="billing_info"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment_method/", views.payment_method, name="payment_method"),
    path("process_order", views.process_order, name="process_order"),
]