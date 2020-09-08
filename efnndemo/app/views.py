from django.shortcuts import render

# Create your views here.


def Home(req, *args, **kwargs):
    return render(req, template_name = 'index.html')