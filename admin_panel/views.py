from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def filters(request):
    return render(request, 'filters_page.html')