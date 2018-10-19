from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def filters(request):
    ctx = {}
    return render(request, 'filters_page.html', ctx)


def create_filter(request):
    ctx = {}


    return render(request, 'create_filter.html', ctx)
