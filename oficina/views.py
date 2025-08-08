from django import forms
from django.shortcuts import render, redirect
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
    page_obj = Paginator(oficinas, 10).get_page(request.GET.get('page'))
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

