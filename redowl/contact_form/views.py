from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .forms import ContactForm

def tg_form(request):

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        return HttpResponseRedirect('/')