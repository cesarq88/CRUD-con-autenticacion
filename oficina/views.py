from django.shortcuts import render
from .models import Oficina
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def oficina_list(request):
    oficinas = Oficina.objects.all().order_by('nombre')

    paginator = Paginator(oficinas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'oficina/oficina_list.html', {'page_obj': page_obj})

    
# Create your views here.
