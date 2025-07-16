from django.http import HttpResponse

def index(request):
    return HttpResponse("Chào mừng đến với LocalLibrary!")

