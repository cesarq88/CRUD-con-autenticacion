# persona/views.py
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect, get_object_or_404 
from .models import Persona
from django import forms
from django.contrib import messages
from oficina.models import Oficina
from django.core.files.base import ContentFile 
from django.core.files.storage import default_storage
from django.views.decorators.http import require_http_methods 
import csv , io 


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellido', 'nombre', 'edad', 'oficina']

@login_required
def persona_list(request):
    q = (request.GET.get('q') or '').strip()

   
    personas_qs = Persona.objects.select_related('oficina').all()

    if q:
        personas_qs = personas_qs.filter(
            Q(apellido__icontains=q) | Q(nombre__icontains=q)
        )

    personas_qs = personas_qs.order_by('apellido', 'nombre')

    paginator = Paginator(personas_qs, 5) 
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'persona/persona_list.html', {
        'page_obj': page_obj,
        'q': q,
    })
@login_required

def persona_create(request): 
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('persona:persona_list')
    else:
        form = PersonaForm()
    return render(request, 'persona/persona_form.html', {'form': form})

@login_required
def persona_update(request, pk):
    persona =  get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('persona:persona_list')
    else:
        form = PersonaForm(instance=persona)
    return render(request, 'persona/persona_form.html', {'form': form})

@login_required
def persona_delete(request, pk):
    persona =  get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        persona.delete()
        return redirect('persona:persona_list')
    return render(request, 'persona/persona_confirm_delete.html', {'persona': persona})

@login_required
def persona_detail(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    return render(request, 'persona/persona_detail.html', {'persona': persona}) 

@login_required
@require_http_methods(["GET", "POST"])
def persona_importar(request):
    if request.method == "POST" and request.FILES.get("archivo"):
        f = request.FILES["archivo"]
        tmp = default_storage.save(f"uploads/{f.name}", ContentFile(f.read()))
        creadas = 0
        with default_storage.open(tmp, "rb") as fh:   # abrir binario
            text_file = io.TextIOWrapper(fh, encoding="utf-8")  # envolver con encoding
            reader = csv.DictReader(text_file)
            for row in reader:
                apellido = (row.get("apellido") or "").strip()
                nombre = (row.get("nombre") or "").strip()
                edad_raw = (row.get("edad") or "").strip()
                oficina_nombre = (row.get("oficina") or "").strip()
                if not (apellido and nombre and oficina_nombre):
                    continue
                try:
                    edad = int(edad_raw) if edad_raw else 0
                except ValueError:
                    edad = 0
                oficina, _ = Oficina.objects.get_or_create(
                    nombre=oficina_nombre, defaults={"nombre_corto": ""}
                )
                Persona.objects.create(apellido=apellido, nombre=nombre, edad=edad, oficina=oficina)
                creadas += 1
        messages.success(request, f"Personas — creadas: {creadas}.")
        return redirect("persona:persona_list")
    return render(request, "persona/persona_importar.html")