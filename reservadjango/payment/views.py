from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView, TemplateView
from .forms import Shipping_form, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from accounts.models import CustomUser, Profile
from reservadjango.models import Servicio
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart import Cart


# Create your views here.
def payment_success(request):
    render (request, "payments/payment_success.html",{})



@login_required
def billing_info(request):
    if request.user.is_authenticated:
        current_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = Shipping_form(request.POST or None, instance=current_user)

        if shipping_form.is_valid():
            shipping_form.save()
            messages.success(request, "Tu informacion de facturacion se ha actualizado.")
            return redirect('index')
        return render(request, 'payments/billing_info.html', {'shipping_form':shipping_form})
    else:
        messages.success(request, "Debes iniciar sesion para acceder a esta página.")
        return redirect('index')
    


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    cantidades = cart.get_cantidades
    totals = cart.cart_total()

    if request.user.is_authenticated:
        current_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = Shipping_form(request.POST or None, instance=current_user) 
        return render(request, "payments/checkout.html",{'cart_products':cart_products, "cantidades":cantidades, "totals":totals, "form":form})

    else:
        #checkout sin usuario
        form = Shipping_form(request.POST or None)
        return render(request, "payments/checkout.html",{'cart_products':cart_products, "cantidades":cantidades, "totals":totals, "form":form})
    

def payment_method(request):
    if request.POST:
        cart = Cart(request)
        totals = cart.cart_total()
        
        #create session with billing info

        my_shipping = request.POST
        request.session['my_shipping']= my_shipping

        if request.user.is_authenticated:
            #checkear si esta logeado y obtener la informacion de pago

            billing_form = PaymentForm()
            return render(request, "payments/method.html", {"totals": totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
            billing_form = PaymentForm()
            return render(request,"payments/method.html", {"totals": totals, "shipping_info":request.POST, "billing_form":billing_form})
        
    else:
        messages.success(request, "Acceso denegado.")
        return redirect('index')
    

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products()
        cantidades = cart.get_cantidades()
        totals = cart.cart_total()
        metodo = request.POST.get('metodo_de_pago')
        payment_form = PaymentForm(request.POST or None)
        #get shipping session data
        my_shipping = request.session.get('my_shipping')

        #generar Order info
        
        full_name = my_shipping['shipping_nombre']
        email = my_shipping['shipping_email']
        precio = totals
        shipping_address = f"Nombre: {my_shipping['shipping_nombre']}\nEmail: {my_shipping['shipping_email']}\nCI: {my_shipping['shipping_cedula']}\nDirección: {my_shipping['shipping_direccion']}\nCiudad: {my_shipping['shipping_ciudad']}\nMétodo de pago: {metodo}"


        if request.user.is_authenticated:
            user = request.user
            #CREAR ORDEN
            create_order = Order(user=user,nombre=full_name, email=email, shipping_address=shipping_address, precio=precio)
            create_order.save()

            #AGREGAR ORDER ITEMS
            #get order id
            order_id = create_order.pk
            for servicio in cart_products:
                servicio_id = servicio.id
                if servicio.descuento:
                    servicio_precio = servicio.precio_descuento
                else:
                    servicio_precio = servicio.precio
                
                for key, value in cantidades.items():
                    if int(key) == servicio_id:
                        create_order_item = OrderItem(order_id=order_id, servicio_id=servicio_id, user=user, cantidad=value, precio=servicio_precio)
                        create_order_item.save()
            #delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
                        

        else:
            create_order = Order(nombre=full_name, email=email, shipping_address=shipping_address, precio=precio)
            create_order.save()
             #AGREGAR ORDER ITEMS
            #get order id
            order_id = create_order.pk
            for servicio in cart_products():
                servicio_id = servicio.id
                if servicio.descuento:
                    servicio_precio = servicio.precio_descuento
                else:
                    servicio_precio = servicio.precio
                
                for key, value in cantidades().items():
                    if int(key) == servicio_id:
                        create_order_item = OrderItem(order_id=order_id, servicio_id=servicio_id, cantidad=value, precio=servicio_precio)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

        messages.success(request, f"Orden creada. Orden número {order_id}.")
        return redirect('index')
