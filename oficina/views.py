from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Oficina

class OficinaForm(forms.ModelForm):
    class Meta:
        model = Oficina
        fields = ['nombre', 'nombre_corto']

@login_required
def oficina_list(request):
    oficinas = Oficina.objects.all().order_by('nombre')
    page_obj = Paginator(oficinas, 5).get_page(request.GET.get('page'))
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

