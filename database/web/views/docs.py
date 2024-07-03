from django.shortcuts import render, redirect

def documentation(request):
    return redirect('/static/docs/index.html')
