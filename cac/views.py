from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.template import loader

from cac.forms import ContactoForm

from django.contrib import messages

from django.views.generic import ListView, View


from cac.models import Categoria
from cac.forms import ContactoForm, CategoriaForm, CategoriaFormValidado

# Create your views here.

def index(request):

    listado_cursos = [
        {
            'nombre': 'Fullstack Java',
            'descripcion': 'Curso de Fullstack',
            'categoria': 'Programación'
        },
        {
            'nombre': 'Diseño UX / UI',
            'descripcion': 'Curso de diseño y navegabilidad',
            'categoria': 'Diseño'
        },
        {
            'nombre': 'Big Data',
            'descripcion': 'Test',
            'categoria': 'Análisis de datos'
        },
    ]
    
    
    if(request.method == 'POST'):
        contacto_form = ContactoForm(request.POST)
        if(contacto_form.is_valid()):
            #enviar un email al administrado con los datos
            #guardar los datos en la base
            messages.success(request,'Muchas gracias por contactarte, te esteremos respondiendo en breve.')
            messages.info(request,'Otro mensajito')
            #deberia validar y realizar alguna accion
        else:
            messages.warning(request,'Por favor revisa los errores')
    else:
        contacto_form = ContactoForm()

    return render(request,'cac/publica/index.html',
                {'cursos':listado_cursos,'contacto_form':contacto_form})
    
def quienes_somos(request):
    # return redirect('saludar_por_defecto')
    # return redirect(reverse('saludar', kwargs={'nombre': 'Diego'}))
    template = loader.get_template('cac/publica/quienes_somos.html')
    context = {
        'titulo': 'Codo a Codo - Quienes somos'
    }
    return HttpResponse(template.render(context, request))

def ver_proyectos(request, anio=2022, mes=1):
    proyectos = []
    return render(request, 'cac/publica/proyectos.html', {'proyectos': proyectos})

def ver_cursos(request, anio=2022, mes=1):
    listado_cursos = [
        {
            'nombre': 'Fullstack Java',
            'descripcion': 'Curso de Fullstack',
            'categoria': 'Programación'
        },
        {
            'nombre': 'Diseño UX / UI',
            'descripcion': 'Curso de diseño y navegabilidad',
            'categoria': 'Diseño'
        },
        {
            'nombre': 'Big Data',
            'descripcion': 'Test',
            'categoria': 'Análisis de datos'
        },
    ]
    return render(request, 'cac/publica/cursos.html', {'cursos': listado_cursos})

def index_administracion(request):
    variable = 'test variable'
    return render(request, 'cac/administracion/index_administracion.html', {'variable': variable})


def api_proyectos(request,):
    proyectos = [{
        'autor': 'Gustavo Villegas',
        'portada': 'https://agenciadeaprendizaje.bue.edu.ar/wp-content/uploads/2021/12/Gustavo-Martin-Villegas-300x170.png',
        'url':'https://marvi-artarg.web.app/'
    },{
        'autor': 'Enzo Martín Zotti',
        'portada': 'https://agenciadeaprendizaje.bue.edu.ar/wp-content/uploads/2022/01/Enzo-Martin-Zotti-300x170.jpg',
        'url':'https://hablaconmigo.com.ar/'
    },{
        'autor': 'María Echevarría',
        'portada': 'https://agenciadeaprendizaje.bue.edu.ar/wp-content/uploads/2022/01/Maria-Echevarria-300x170.jpg',
        'url':'https://compassionate-colden-089e8a.netlify.app/'
    },]
    response = {'status':'Ok','code':200,'message':'Listado de proyectos','data':proyectos}
    return JsonResponse(response,safe=False)


def categorias_index(request):
    #queryset
    categorias = Categoria.objects.filter(baja=False)
    return render(request,'cac/administracion/categorias/index.html',{'categorias':categorias})

def categorias_nuevo(request):
    if(request.method=='POST'):
        formulario = CategoriaFormValidado(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('categorias_index')
    else:
        formulario = CategoriaFormValidado()
    return render(request,'cac/administracion/categorias/nuevo.html',{'formulario':formulario})


def categorias_editar(request,id_categoria):
    try:
        categoria = Categoria.objects.get(pk=id_categoria)
    except Categoria.DoesNotExist:
        return render(request,'cac/administracion/404_admin.html')

    if(request.method=='POST'):
        formulario = CategoriaFormValidado(request.POST,instance=categoria)
        if formulario.is_valid():
            formulario.save()
            return redirect('categorias_index')
    else:
        formulario = CategoriaFormValidado(instance=categoria)
    return render(request,'cac/administracion/categorias/editar.html',{'formulario':formulario})
    

def categorias_eliminar(request,id_categoria):
    try:
        categoria = Categoria.objects.get(pk=id_categoria)
    except Categoria.DoesNotExist:
        return render(request,'cac/administracion/404_admin.html')
    categoria.soft_delete()
    return redirect('categorias_index')


class CategoriasListView(ListView):
    model = Categoria
    context_object_name = 'lista_categorias'
    template_name= 'cac/administracion/categorias/index.html'
    queryset= Categoria.objects.filter(baja=False)
    ordering = ['nombre']


class CategoriasView(View):
    form_class = CategoriaFormValidado
    template_name = 'cac/administracion/categorias/nuevo.html'

    def get(self, request,*args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name,{'formulario':form})
    
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias_index')
        return render(request,self.template_name,{'formulario':form})


def hola_mundo(request):
    return HttpResponse('Hola Mundo Django')

def saludar(request, nombre="Pepe"):
    return HttpResponse(f"Hola Mundo - {nombre}")



def cursos_detalle(request, nombre_curso):
    return HttpResponse(f"""
        <h1>{nombre_curso}</h1>
    """)

def cursos(request, nombre):
    return HttpResponse(f"""
        <h2>{nombre}</h2>
    """)



def categorias_index(request):
    #queryset
    categorias = Categoria.objects.filter(baja=False)
    return render(request,'cac/administracion/categorias/index.html',{'categorias':categorias})

def categorias_nuevo(request):
    if(request.method=='POST'):
        formulario = CategoriaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            nueva_categoria = Categoria(nombre=nombre)
            nueva_categoria.save()
            return redirect('categorias_index')
    else:
        formulario = CategoriaForm()
    return render(request,'cac/administracion/categorias/nuevo.html',{'formulario':formulario})


def categorias_eliminar(request,id_categoria):
    try:
        categoria = Categoria.objects.get(pk=id_categoria)
    except Categoria.DoesNotExist:
        return render(request,'cac/administracion/404_admin.html')
    categoria.soft_delete()
    return redirect('categorias_index')