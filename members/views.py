from django.shortcuts import render

def dashboard(request):
    context = {
        'nama': 'Mr. John William Doe',
        'role': 'Member', 
    }
    return render(request, 'members/dashboard.html', context)

def list_member(request):
    context = {
        'role': 'Staff',  
        'nama': 'Mr. John William Doe',
    }
    return render(request, 'members/list_member.html', context)

def form_member(request):
    return render(request, 'members/form_member.html')