from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
# este def lo que hace si el usuaario se registra por primera vez
# le muestra un formulario para completar sus datos
#si se se envia el formulario y es valido, se guarda el usuario
# si el capthcha no es valido   no crea nada y se muestra los errores 
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts_app/register.html', {'form': form})


#def home(request):
 #   return render(request, 'accounts_app/home.html')
def home(request):
    if request.user.is_authenticated:
        return redirect('oficina_list')     # ya logueado → a Oficinas
    return redirect('login') 


# Create your views here.
