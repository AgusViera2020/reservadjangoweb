from django import forms
from .models import ShippingAddress


class Shipping_form(forms.ModelForm):
    shipping_nombre = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre y apellido'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    shipping_cedula= forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cedula'}), required=True)
    shipping_direccion = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección'}), required=True)
    shipping_ciudad = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ciudad'}), required=True)

    class Meta:
        model = ShippingAddress 
        fields = ['shipping_nombre', 'shipping_email','shipping_cedula', 'shipping_direccion','shipping_ciudad',]
        exclude = ['user',]


class PaymentForm(forms.Form):
    metodo_de_pago = forms.ChoiceField(choices=[('1','Retiro en sucursal'),('2','Tarjeta de débito/crédito')], widget=forms.Select(attrs={'class':'form-select', 'placeholder':'Método de pago' }), required=True)
    tarjeta_nombre= forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titular de la tarjeta'}))
    tarjeta_numero= forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número tarjeta'}))
    tarjeta_vencimiento= forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fecha de vencimiento'}))
    cvv= forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código de seguridad'}))
