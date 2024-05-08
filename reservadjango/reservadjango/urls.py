"""
URL configuration for reservadjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from django.views.generic.base import TemplateView  # new
from django.contrib.auth.decorators import login_required
from .views import index, servicio, categoria, search, reservar, filter_products, all_services, mis_reservas
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("cart/", include ("cart.urls")),
    path("payment/", include ("payment.urls")),
    path("", index, name="index"),
    path("reserva/", reservar, name="reserva"),
    path("mis_reservas/", mis_reservas, name="mis_reservas"),
    path("obtener_horas/", views.obtener_horas, name="obtener_horas"),
    path("servicio/<int:pk>", servicio, name ="servicio_detalle"),
    path("categoria/<str:foo>", categoria, name = "categoria"),
    path("search/", search, name='search'),
    path("filter_products/", filter_products, name='filter_products'),
    path("all_services/", all_services, name='all_services'),


] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)