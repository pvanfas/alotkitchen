from django.shortcuts import render

from main.models import Area


def index(request):
    template_name = "web/index.html"
    context = {}
    return render(request, template_name, context)


def page_view(request, slug):
    template_name = "web/page.html"
    area = Area.objects.get(slug=slug)
    context = {"area": area}
    return render(request, template_name, context)
