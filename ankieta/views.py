from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse,Http404, HttpResponseRedirect
from .models import Pytanie, Odpowiedz


def index(request):
    ostatnie_ankiety=Pytanie.objects.order_by('-data_publikowacji')[:5]
    context={'ostatnie_ankiety':ostatnie_ankiety,}
    return render(request,'ankieta/index.html',context)



def szczegoly(request,pytanie_id):
    try:
        pytanie=Pytanie.objects.get(pk=pytanie_id)
    except Pytanie.DoesNotExist:
        return render(request, 'ankieta/blad.html',status=404)
    return render(request, 'ankieta/szczegoly.html', {'pytanie':pytanie})


def glosuj(request,pytanie_id):
    pytanie=get_object_or_404(Pytanie, pk=pytanie_id)
    try:
        wybr_odp=pytanie.odpowiedz_set.get(pk=request.POST['odp'])
    except (KeyError, Odpowiedz.DoesNotExist):
        return render(request, 'ankieta/szczegoly.html',{
            'pytanie':pytanie,
            'error_message': 'Nie wybrales niczego!!!'
        })
    else:
        wybr_odp.glosy+=1
        wybr_odp.save()
        return HttpResponseRedirect(reverse('wyniki', args=(pytanie.id,)))  

def wyniki(request,pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    return render(request,'ankieta/wyniki.html',{'pytanie':pytanie})
