from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView, TemplateView
from .forms import CustomUserCreationForm, LoginForm, PassChangeForm, CustomUserChangeForm, UserInfoForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import CustomUser, Profile
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from cart.cart import Cart

    
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:update_user_info")
    template_name = "registration/signup.html"
    success_message = "Cuenta creada correctamente."
    login_url = "accounts/login/"

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add a success message
        user = form.save()
        login(self.request, user)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        # Get the errors from the form
        errors = form.errors
        for field_name, error_messages in errors.items():
            # Loop through each field's error messages and add them to the messages framework
            for error_message in error_messages:
                messages.error(self.request, f"Error: {error_message}")
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Redirect logged-in users to index page
        return super().dispatch(request, *args, **kwargs)


class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    login_url ='/accounts/login/'
    form_class = PassChangeForm
    template_name = "registration/password_change.html"
    success_message = "Contraseña actualizada correctamente."

    def form_invalid(self, form):
        errors = form.errors
        for field_name, error_messages in errors.items():
            for error_message in error_messages:
                messages.error(self.request, f"Error: {error_message}")
        return super().form_invalid(form)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Add a success message
        messages.success(self.request, self.success_message)
        return response

@login_required
def pass_success (request):
    nombre = request.user.nombre.capitalize()
    message = f"{nombre} su contraseña fue actualizada con éxito"
    return render(request, 'registration/password_change_done.html', {"message":message})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            print(password)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                current_user = Profile.objects.get(user__id = request.user.id)
                #get their saved cart from db
                saved_cart =  current_user.old_cart
                if saved_cart:
                    converted_cart = json.loads(saved_cart)
                    #add cart to session
                    cart = Cart(request)
                    #loop through cart and add items
                    for key, value in converted_cart.items():
                        cart.db_add(servicio=key, cantidad=value)


                return redirect('/')
            else:
                error = "Las credenciales son incorrectas."
                return render(request, 'registration/login.html', {'form':form, 'error':error} )

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})

@login_required
def update_user(request):
        if request.user.is_authenticated:
            current_user = CustomUser.objects.get(id=request.user.id)
            user_form = CustomUserChangeForm(request.POST or None, instance=current_user)

            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, "Usuario actualizado correctamente.")
                return redirect('index')
            return render(request, 'registration/profile_view.html', {'user_form':user_form})
        else:
            messages.success(request, "Debes iniciar sesion para acceder a esta página.")
            return redirect('index')

@login_required
def update_user_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        user_form = UserInfoForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Tu informacion se ha actualizado correctamente.")
            return redirect('index')
        return render(request, 'registration/update_user_info.html', {'user_form':user_form})
    else:
        messages.success(request, "Debes iniciar sesion para acceder a esta página.")
        return redirect('index')




def email_check(request):
    email = request.GET.get('email')
    if CustomUser.objects.filter(email=email).exists():
        available = False
    else:
        available = True
    print(available)
    return JsonResponse({'available': available})


    


            







