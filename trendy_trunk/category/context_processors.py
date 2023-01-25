from . models import Category

# links generating fumction
def menu_links(request):
    links=Category.objects.all()
    return dict(links=links) 