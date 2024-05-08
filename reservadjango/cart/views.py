from django.shortcuts import render, get_object_or_404,redirect
from .cart import Cart
from reservadjango.models import Servicio
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products

    cantidades = cart.get_cantidades

    totals = cart.cart_total()
    return render(request, "cart_summary.html",{'cart_products':cart_products, "cantidades":cantidades, "totals":totals})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        try:
            servicio_id = int(request.POST.get('servicio_id'))
            servicio = get_object_or_404(Servicio, id=servicio_id)
            cantidad = int(request.POST.get('cantidad'))
        #save to session
            cart.add(servicio= servicio, cantidad= cantidad)

        #get cart quantity
            cart_quantity = cart.__len__()
            messages.success(request,('Producto agregado al carrito.'))
            response = JsonResponse({'qty: ': cart_quantity})

            return response
        except:
            messages.error(request,('Hubo un error al agregar el producto al carrito.'))
            return JsonResponse({"Error":Exception})

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        try:
            servicio_id = int(request.POST.get('servicio_id'))
            #DELETE
            cart.delete(servicio= servicio_id)
            response = JsonResponse({'servicio': servicio_id})
            messages.success(request,("Producto eliminado."))
            return response
        except Exception:
            messages.error(request, ("Error al eliminar el producto del carrito."))


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        servicio_id = int(request.POST.get('servicio_id'))
        cantidad = int(request.POST.get('cantidad'))

        cart.update(servicio = servicio_id, cantidad=cantidad)

        response = JsonResponse({'qty':cantidad})
        return response
        
            