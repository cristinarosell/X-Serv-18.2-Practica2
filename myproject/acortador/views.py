from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from models import Urls

# Create your views here.


def formulario(request):
    salida = ""

    if request.method == "POST":
        if request.body == "":
            salida += "Error, debe escribir una url"     
        else:
            cuerpo = request.body.split('valor=')[1]
            if cuerpo.find("http") == -1:
                cuerpo = "http://" + cuerpo
            else:
                cuerpo = cuerpo.replace('%3A%2F%2F', '://')
        try: 
            fila=Urls.objects.get(larga=cuerpo)
        except Urls.DoesNotExist:
            fila = Urls(larga=cuerpo)
            fila.save()
            
        salida += "Url larga: " + "<a href='" + fila.larga
        salida += "'>" + fila.larga + "</a>" + "</br>"
        salida += "Url corta: " + "<a href='" + str(fila.id)
        salida += "'>" + str(fila.id) + "</a>" + "</br>"
         
    elif request.method == "GET":
        salida += '<form action="" method="POST">'
        salida += 'Introducir url : <input type="text" name="valor">'
        salida += '<input type="submit" value="Enviar">'
        salida += '</form>'
        
        lista = Urls.objects.all()
        salida += "</br></br>Las urls que hay son:<ul>"
        for fila in lista:
            salida += "<li> Url larga: " + fila.larga 
            salida += "  -->  Url Corta: " + str(fila.id)
        salida += "</ul>"
                      
        
    return HttpResponse(salida)


def redirigir(request, recurso):
    try:
        fila = Urls.objects.get(id=recurso)
    except Urls.DoesNotExist:
        return HttpResponse("Error, la url corta no es valida")
    return HttpResponseRedirect(fila.larga)
    
    
