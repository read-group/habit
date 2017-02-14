from django.shortcuts import render

# Create your views here.
def index(request):
    request.session['hello']='world'
    return render(request,"front/index.html");
