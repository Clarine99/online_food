from django.shortcuts import render
from django.http import HttpResponse

def home (request):
    if request.user:
        user = request.user
        context ={
            'user':user}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')