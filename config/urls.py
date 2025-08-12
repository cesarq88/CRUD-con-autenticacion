from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', include('accounts_app.urls')), 
    path('', include('oficina.urls')),        
    path('captcha/', include('captcha.urls')),
    path('', include('persona.urls')),
]
