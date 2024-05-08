from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
import datetime
from . import google_calendar
import locale
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Servicio, Categoria, Reserva
from django.utils import timezone


locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


def reservar(request):
    current_datetime = datetime.datetime.now()
    calendar_manager = google_calendar.GoogleCalendarManager()
    busy_hours, available_hours = calendar_manager.list_busy_available_events(current_datetime)

    try:
        nombre = request.user.nombre.capitalize()
        apellido = request.user.apellido.capitalize()
        telefono = request.user.telefono
    except AttributeError:
        pass

    if request.method == 'POST':
        user = request.user
        
        if not request.user.is_authenticated:
            return JsonResponse({'error_message': 'Debes iniciar sesión para realizar una reserva.'})

        print(nombre, apellido ,telefono)
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        servicio = request.POST.get('servicio')
        
        if nombre =="Ingrese su nombre" or nombre == None or nombre =='' or telefono == "Ingrese un teléfono de contacto" or telefono == None or telefono == '' or hora == "Elija una hora..." or hora =='' or servicio == None or servicio =='' or servicio == "Elija un servicio...":
            return JsonResponse({'error_message': 'Por favor completa todos los campos antes de realizar la reserva.'})
        
        selected_datetime = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        fecha_formateada = selected_datetime.strftime('%d de %B')

        selected_datetime = datetime.datetime.combine(selected_datetime, datetime.datetime.strptime(hora, "%H:%M").time())
        if selected_datetime > current_datetime:
            validation = True
        else:
            validation = False

        if validation == True:
            start_time = selected_datetime.isoformat()
            end_time = (selected_datetime + datetime.timedelta(minutes=30)).isoformat()
            success = calendar_manager.create_event(servicio + ". " + nombre + ". Contacto: " + telefono, start_time, end_time, "America/Argentina/Buenos_Aires")
            crear_reserva = Reserva(user=user, nombre=nombre, servicio=servicio, fecha=fecha, hora=hora, contacto=telefono)
            crear_reserva.save()
            if success == 200:
                success_message = f"Tu cita fue reservada para el día {fecha_formateada}, a las {hora} horas. Te esperamos."
                return JsonResponse({'success_message': success_message})
            else:
                error_message = "Hubo un error al crear tu cita, por favor inténtalo de nuevo más tarde."
                return JsonResponse({'error_message': error_message})
        else:
            return JsonResponse({'error': 'Ha seleccionado una hora en el pasado, por favor seleccione una nueva' })
            
    if request.method =='GET':
        if not request.user.is_authenticated:
            return render(request, 'reservar.html', {'available_hours':available_hours})
        else:
            return render(request, 'reservar.html', {'apellido':apellido,'nombre':nombre, 'telefono':telefono, 'available_hours':available_hours})
        
@login_required
def mis_reservas(request):
    if request.user.is_authenticated:
        user = request.user
        now = timezone.now()
        reservas = Reserva.objects.filter(user__id=user.id, fecha__gt=now)
        if request.method == 'POST':
            reserva_id = request.POST['reserva_id']
            print('Reserva numero: ', reserva_id)
            reserva = get_object_or_404(Reserva, id=reserva_id, user=user)
            print(reserva)
            reserva.delete()
            return JsonResponse({'message':'Su reserva ha sido eliminada.'})
        return render(request, 'mis_reservas.html',{'reservas':reservas})


def index(request):
    servicios = Servicio.objects.all()
    categorias = Categoria.objects.all()
    context = {'servicios':servicios, 'categorias':categorias}

    if request.method == 'POST':
        buscar = request.POST['buscar']
        print(buscar)
        result = Servicio.objects.filter(nombre__icontains= buscar)
        if not result:
            messages.success(request, ("Producto no encontrado"))

        return render(request, 'index.html', {'servicios':servicios, 'categorias':categorias, 'result':result, 'buscar':str(buscar).capitalize()})

    if request.method =='GET':
        return render(request, 'index.html', context)

def filter_products(request):
    if request.method == 'GET' and 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        categorias = Categoria.objects.all()
        selected_categories = request.GET.getlist('categories[]')
        print(selected_categories)
        servicios = Servicio.objects.filter(categoria__id__in=selected_categories)
        print(servicios)
        rendered_services = render_to_string('servicios_partial.html', {'servicios': servicios})
        return JsonResponse({'servicios': rendered_services})



def obtener_horas(request):
    if request.method == 'GET' and 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        fecha_seleccionada = request.GET.get('fecha')
        fecha_seleccionada = datetime.datetime.strptime(fecha_seleccionada, '%Y-%m-%d')
        calendar_manager = google_calendar.GoogleCalendarManager()
        busy_hours, available_hours = calendar_manager.list_busy_available_events(fecha_seleccionada)
        return JsonResponse({'horas_disponibles': available_hours})
    return JsonResponse({'error': 'Método no permitido'})


def servicio(request, pk):
    servicio = Servicio.objects.get(id=pk)
    return render(request, 'servicio.html', {'servicio':servicio})


def categoria(request, foo):
    foo = foo.replace('-',' ')
    if request.method=='GET':
        try:
            categoria = Categoria.objects.get(nombre = foo)
            print(categoria)
            servicios = Servicio.objects.filter(categoria=categoria)
            print(servicios)
            return render(request, 'categorias.html', {"servicios":servicios, "categorias":categoria})
        except:
            messages.success(request, ("La categoría ingresada no existe."))
            return redirect(request, 'index')


def search(request):
    return render(request, 'search.html',{})

def all_services(request):
    all_servicios = Servicio.objects.all()

    servicios_html = render_to_string('servicios_partial.html', {'servicios': all_servicios})

    return JsonResponse({'servicios': servicios_html})