from django.shortcuts import render

# Create your views here.
#from django.http import render

# Create your views here.
def index(request):
    return render(request,'blog/index.html')
