from django.shortcuts import render

def list_member(request):
    return render(request, 'list_member.html')

def form_member(request):
    return render(request, 'form_member.html')