from django.shortcuts import render, redirect

def dashboard(request):
    context = {
        'nama': 'Mr. John William Doe',
        'role': 'Staff', 
    }
    return render(request, 'members/dashboard.html', context)

def list_member(request):
    context = {
        'role': 'Staff',  
        'nama': 'Mr. John William Doe',
    }
    return render(request, 'members/list_member.html', context)

def list_identitas(request):
    context = {
        'role': 'Member',
        'nama': 'Mr. John Doe',
    }
    return render(request, 'members/identitas.html', context)

def form_member(request):
    return render(request, 'members/form_member.html')


def login_page(request):
    context = {
        'demo_account': {
            'email': 'john@example.com',
            'password': '******',
            'role': 'Member',
        }
    }
    return render(request, 'members/login.html', context)


def logout_page(request):
    # Simulasi menghapus session dengan cara redirect ke login
    return redirect('login_page')


def register_page(request):
    context = {
        'sample_members': [
            {'nama': 'Alice Pramesti', 'email': 'alice@mail.com', 'status': 'Aktif'},
            {'nama': 'Raka Mahendra', 'email': 'raka@mail.com', 'status': 'Menunggu Verifikasi'},
        ]
    }
    return render(request, 'members/register.html', context)


def profile_settings(request):
    role = request.GET.get('role', 'Member')
    if role == 'Staff':
        context = {
            'role': 'Staff',
            'nama': 'Mr. Admin Aero',
            'email': 'admin@aeromiles.com',
            'nama_depan': 'Admin',
            'nama_belakang': 'Aero',
        }
    else:
        context = {
            'role': 'Member',
            'nama': 'Mr. John Doe',
            'email': 'john@example.com',
            'nama_depan': 'John',
            'nama_belakang': 'Doe',
        }
    return render(request, 'members/profile_settings.html', context)