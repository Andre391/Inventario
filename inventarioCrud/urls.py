"""
URL configuration for inventarioCrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup, name='signup'),
    path('elementos/', views.elementos, name='elementos'),
    path('elementos/create',views.crear_elemento, name='crear_elemento'),
    path('elementos/<int:elemento_id>/',views.elemento_detail, name='elemento_detail'),
    path('elementos/<int:elemento_id>/delete',views.delete_elemento, name='delete_elemento'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('signin/', views.signin, name='signin'),
    
    
]
