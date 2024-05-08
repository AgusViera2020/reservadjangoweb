from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(required=True, label="Nombre", max_length=30)
    apellido = forms.CharField(required=True, label="Apellido", max_length=30)
    email = forms.EmailField(required=True, label="Correo electrónico", max_length=50)
    telefono = forms.IntegerField(required=True, label="Teléfono de contacto")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('nombre','apellido','email','telefono','password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este email.")
        return email
    
    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas deben coincidir.")
        
        if len(password1) <6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres")
        return super().clean_password2()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['apellido'].required = True
        self.fields['email'].required = True
        self.fields['telefono'].required= True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data["nombre"]
        user.apellido = self.cleaned_data["apellido"]
        user.email = self.cleaned_data["email"]
        user.telefono = self.cleaned_data["telefono"]
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", max_length=50, widget=forms.EmailInput)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class PassChangeForm(forms.Form):
    old_password = forms.CharField(label="Contraseña antigua", max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(label="Nueva Contraseña", max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(label="Repetir contraseña", max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("La contraseña antigua es incorrecta.")
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("Las nuevas contraseñas no coinciden.")
        return new_password2

    def save(self, commit=True):
        new_password = self.cleaned_data["new_password1"]
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user


class CustomUserChangeForm(UserChangeForm):
    password = None
    nombre = forms.CharField(label="Nombre", max_length="50", widget=forms.TextInput(attrs={'class':'form-control'}))
    apellido = forms.CharField(label="Apellido", max_length="50", widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Email", max_length="50", widget=forms.EmailInput(attrs={'class':'form-control'}))
    telefono =forms.IntegerField(label="Teléfono de contacto", widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = CustomUser
        fields = ("nombre","apellido","email", "telefono")


class UserInfoForm(forms.ModelForm):
    #foto = forms.
    direccion = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección'}), required=False)
    pais = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pais'}), required=False)
    ciudad = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ciudad'}), required=False)

    class Meta:
        model = Profile 
        fields = ('direccion', 'pais', 'ciudad')