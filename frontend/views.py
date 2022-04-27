from django.shortcuts import render


def Index(request):
    return render(request, 'frontend/index.html')
