from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Oficina
from django.core.files.base import ContentFile 
from django.core.files.storage import default_storage
from django.contrib import messages 
from django.views.decorators.http import require_http_methods
import csv , io

class OficinaForm(forms.ModelForm):
    class Meta:
        model = Oficina
        fields = ['nombre', 'nombre_corto']

@login_required
def oficina_list(request):
    oficinas = Oficina.objects.all().order_by('nombre')
    page_obj = Paginator(oficinas, 5
    ).get_page(request.GET.get('page'))
    return render(request, 'oficina/oficina_list.html', {'page_obj': page_obj})

@login_required
def oficina_create(request):
    if request.method == 'POST':
        form = OficinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('oficina_list')
    else:
        form = OficinaForm()
    return render(request, 'oficina/oficina_form.html', {'form': form})

@login_required
def oficina_update(request, pk):
    oficina = get_object_or_404(Oficina, pk=pk)
    if request.method == 'POST':
        form = OficinaForm(request.POST, instance=oficina)
        if form.is_valid():
            form.save()
            return redirect('oficina_list')
    else:
        form = OficinaForm(instance=oficina)
    return render(request, 'oficina/oficina_form.html', {'form': form})

@login_required
def oficina_delete(request, pk):
    oficina = get_object_or_404(Oficina, pk=pk)
    if request.method == 'POST':
        oficina.delete()
        return redirect('oficina_list')
    return render(request, 'oficina/oficina_confirm_delete.html', {'oficina': oficina})

@login_required
def oficina_detail(request, pk):
    oficina = get_object_or_404(Oficina, pk=pk)
    personas = oficina.persona_set.all().order_by('apellido', 'nombre')
    return render(request, 'oficina/oficina_detail.html', {
        'oficina': oficina,
        'personas': personas
    })

@login_required
@require_http_methods(["GET", "POST"])
def oficina_importar(request):
    if request.method == "POST" and request.FILES.get("archivo"):
        f = request.FILES["archivo"]
        tmp = default_storage.save(f"uploads/{f.name}", ContentFile(f.read()))
        creadas, actualizadas = 0, 0

       
        with default_storage.open(tmp, "rb") as fh:
            text_file = io.TextIOWrapper(fh, encoding="utf-8")
           
            reader = csv.DictReader(text_file)

            for row in reader:
                nombre = (row.get("nombre") or "").strip()
                nombre_corto = (row.get("nombre_corto") or "").strip()
                if not nombre:
                    continue

                obj, created = Oficina.objects.get_or_create(
                    nombre=nombre,
                    defaults={"nombre_corto": nombre_corto}
                )
                if created:
                    creadas += 1
                else:
                    
                    if nombre_corto and obj.nombre_corto != nombre_corto:
                        obj.nombre_corto = nombre_corto
                        obj.save()
                        actualizadas += 1

        messages.success(request, f"Oficinas — creadas: {creadas}, actualizadas: {actualizadas}.")
        return redirect("oficina_list")

    return render(request, "oficina/oficina_importar.html")



