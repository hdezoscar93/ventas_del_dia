# from django import forms
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.models import User
# from .models import Producto, Venta, DetalleVenta

# class LoginForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
#     )

# class RegistroForm(UserCreationForm):
#     email = forms.EmailField(required=True)
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})

# class ProductoForm(forms.ModelForm):
#     class Meta:
#         model = Producto
#         fields = ['nombre', 'descripcion', 'precio', 'stock']
#         widgets = {
#             'nombre': forms.TextInput(attrs={'class': 'form-control'}),
#             'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'precio': forms.NumberInput(attrs={'class': 'form-control'}),
#             'stock': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

# class VentaForm(forms.ModelForm):
#     class Meta:
#         model = Venta
#         fields = ['pagado']
#         widgets = {
#             'pagado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }

# class DetalleVentaForm(forms.ModelForm):
#     class Meta:
#         model = DetalleVenta
#         fields = ['producto', 'cantidad']
#         widgets = {
#             'producto': forms.Select(attrs={'class': 'form-control'}),
#             'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
#         }

from django import forms
from .models import Venta

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import  Venta



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['nombre_producto', 'cantidad', 'precio_unitario', 'metodo_pago', 'notas']
