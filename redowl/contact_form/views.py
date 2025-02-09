from django.http import HttpResponseRedirect

def tg_form(request):

    if request.method == "POST":
        print(request.POST)
    else:
        return HttpResponseRedirect('/')