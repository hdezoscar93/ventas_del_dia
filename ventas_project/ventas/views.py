# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.utils import timezone
# from datetime import datetime, date
# from .models import Producto, Venta, DetalleVenta
# from .forms import LoginForm, RegistroForm, ProductoForm, DetalleVentaForm
import datetime

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')

#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'¡Bienvenido {username}!')
#                 return redirect('dashboard')
#     else:
#         form = LoginForm()

#     return render(request, 'ventas/login.html', {'form': form})

# def registro_view(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')

#     if request.method == 'POST':
#         form = RegistroForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, '¡Cuenta creada exitosamente!')
#             return redirect('dashboard')
#     else:
#         form = RegistroForm()

#     return render(request, 'ventas/registro.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     messages.info(request, 'Has cerrado sesión exitosamente.')
#     return redirect('login')

# @login_required
# def dashboard(request):
#     hoy = date.today()

#     # Ventas de hoy
#     ventas_hoy = Venta.objects.filter(
#         fecha_venta__date=hoy
#     )

#     total_ventas_hoy = sum(venta.total for venta in ventas_hoy)
#     cantidad_ventas_hoy = ventas_hoy.count()

#     # Productos bajos en stock
#     productos_bajos = Producto.objects.filter(stock__lt=5)

#     context = {
#         'ventas_hoy': ventas_hoy,
#         'total_ventas_hoy': total_ventas_hoy,
#         'cantidad_ventas_hoy': cantidad_ventas_hoy,
#         'productos_bajos': productos_bajos,
#         'hoy': hoy,
#     }

#     return render(request, 'ventas/dashboard.html', context)

# @login_required
# def nueva_venta(request):
#     if request.method == 'POST':
#         descripcion = request.POST.get('descripcion')
#         cantidad = request.POST.get('cantidad')
#         total = request.POST.get('total')

#         # Validaciones básicas
#         if not descripcion or not cantidad or not total:
#             messages.error(request, 'Por favor completa todos los campos')
#             return redirect('nueva_venta')

#         # Crear la venta con valores por defecto
#         venta = Venta.objects.create(
#             usuario=request.user,
#             descripcion=descripcion,
#             cantidad=int(cantidad),
#             total=float(total),
#             # Valores por defecto:
#             categoria='juguete',
#             metodo_pago='efectivo',
#             pagado=True,
#             fecha_venta=timezone.now()
#         )

#         messages.success(request, f'Venta registrada: ${float(total):.2f}')
#         return redirect('dashboard')

#     return render(request, 'ventas/nueva_venta.html')

# @login_required
# def detalle_venta(request, venta_id):
#     venta = get_object_or_404(Venta, id=venta_id)
#     return render(request, 'ventas/detalle_venta.html', {'venta': venta})

# @login_required
# def historial_ventas(request):
#     ventas = Venta.objects.all().order_by('-fecha_venta')[:50]
#     return render(request, 'ventas/historial.html', {'ventas': ventas})

# @login_required
# def productos(request):
#     if request.method == 'POST':
#         form = ProductoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Producto agregado exitosamente.')
#             return redirect('productos')
#     else:
#         form = ProductoForm()

#     productos_list = Producto.objects.all()
#     return render(request, 'ventas/productos.html', {
#         'form': form,
#         'productos': productos_list
#     })
# @login_required
# def eliminar_producto(request, producto_id):
#     producto = get_object_or_404(Producto, id=producto_id)
#     producto.delete()
#     messages.success(request, 'Producto eliminado exitosamente.')
#     return redirect('productos')



from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import LoginForm, RegistroForm
from .forms import VentaForm
from .models import Venta
from datetime import datetime, timedelta


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'ventas/login.html', {'form': form})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('dashboard')
    else:
        form = RegistroForm()

    return render(request, 'ventas/registro.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@login_required
def dashboard(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    hoy = timezone.localdate()

    if fecha_inicio and fecha_fin:
        try:
            inicio = timezone.make_aware(datetime.strptime(fecha_inicio, "%Y-%m-%d"))
            fin = timezone.make_aware(datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1))

            ventas = Venta.objects.filter(
                fecha_registro__gte=inicio,
                fecha_registro__lt=fin
            ).order_by("-fecha_registro")

            rango_activo = True
        except ValueError:
            messages.error(request, "Fechas inválidas, usando fecha actual.")
            ventas = Venta.objects.filter(fecha_registro__date=hoy).order_by("-fecha_registro")
            rango_activo = False
    else:
        ventas = Venta.objects.filter(fecha_registro__date=hoy).order_by("-fecha_registro")
        rango_activo = False

    total_dia = ventas.aggregate(Sum('total'))['total__sum'] or 0
    total_ventas = ventas.count()

    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.save()
            messages.success(request, f'Venta registrada: ${venta.total:.2f}')
            return redirect('dashboard')
    else:
        form = VentaForm()

    return render(request, 'ventas/dashboard.html', {
        'ventas': ventas,
        'total_dia': total_dia,
        'total_ventas': total_ventas,
        'fecha': hoy,
        'form': form,
        'rango_activo': rango_activo,
    })

@login_required
def nuevo_egreso(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('descripcion')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')

        if not nombre_producto or not cantidad or not precio_unitario:
            messages.error(request, 'Por favor completa todos los campos')
            return redirect('dashboard')

        try:
            cantidad = float(cantidad)
            precio_unitario = float(precio_unitario)
        except ValueError:
            messages.error(request, 'Cantidad y precio deben ser numéricos')
            return redirect('dashboard')

        # ⚠️ Multiplicamos por -1 para registrar el egreso
        venta = Venta.objects.create(
            usuario=request.user,
            nombre_producto=nombre_producto,
            cantidad=cantidad,
            precio_unitario=-abs(precio_unitario),  # valor negativo
            metodo_pago='efectivo',
            fecha_registro=timezone.now()
        )

        messages.warning(request, f'🔴 Egreso registrado: ${abs(venta.total):.2f}')
        return redirect('dashboard')

    # Si es GET, mostrar el formulario
    return render(request, 'ventas/nuevo_egreso.html')


@login_required
def nueva_venta(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('descripcion')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')

        if not nombre_producto or not cantidad or not precio_unitario:
            messages.error(request, 'Por favor completa todos los campos')
            return redirect('dashboard')

        try:
            cantidad = float(cantidad)
            precio_unitario = float(precio_unitario)
        except ValueError:
            messages.error(request, 'Cantidad y precio deben ser valores numéricos')
            return redirect('dashboard')

        venta = Venta.objects.create(
            usuario=request.user,
            nombre_producto=nombre_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            metodo_pago='efectivo',
            fecha_registro=timezone.now()
        )

        # Texto dinámico
        tipo = "Egreso" if venta.total < 0 else "Ingreso"
        color = "🔴" if venta.total < 0 else "🟢"

        messages.success(request, f'{color} {tipo} registrado: ${venta.total:.2f}')
        return redirect('dashboard')

    return render(request, 'ventas/nueva_venta.html')
