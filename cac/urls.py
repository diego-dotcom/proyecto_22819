from django.urls import path
from . import views

urlpatterns = [
    path('hola_mundo',views.hola_mundo),
    path('saludar/',views.saludar,name="saludar_por_defecto"),
    path('saludar/<str:nombre>',views.saludar,name="saludar"),
]