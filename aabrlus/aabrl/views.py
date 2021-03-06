from django.shortcuts import render, render_to_response, get_object_or_404
import random, string, json
from django.utils import timezone
from aabrl.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.context_processors import csrf
 
def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('aabrl/index.html', c)
 
def redirect_original(request, encurt_id):
    url = get_object_or_404(Urls, pk=encurt_id)
    url.contador += 1
    url.save()
    return HttpResponseRedirect(url.url_original)
 
def url_encolhida(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        encurt_id = get_short_code()
        b = Urls(url_original=url, encurt_id=encurt_id)
        b.save()
        response_data = {}
#        response_data['url'] = settings.SITE_URL + "/" + encurt_id
        response_data['url'] = "aabrl.us/" + encurt_id
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    return HttpResponse(json.dumps({"Erro": "Alguma coisa deu errada!"}), content_type="application/json")
 
def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        encurt_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=encurt_id)
        except:
            return encurt_id

#class ListaUrls(ListView):
#    template_name = 'listaurls.html'
#    model = Urls
#    context_object_name = 'urls'
#    def url_list(self):
#        url = Urls.objects.all()
#        q = self.request.GET.get('pesquisar_por')

#        if q is not None:
#            url = url.filter(url_original__icontains=q)
#        return url
def url_list(request):
#    nome = request.SHOW.get("busca", '')
#    if not (nome == ''):
    urls = Urls.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')
    return render(request, 'aabrl/listaurls.html', {'urls':urls})
