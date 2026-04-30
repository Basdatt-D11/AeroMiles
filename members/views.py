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


def kelola_hadiah(request):
    context = {
        'role': 'Staff',
        'nama': 'Mr. Admin Aero',
        'hadiah_list': [
            {
                'kode': 'RWD-001',
                'nama': 'Tiket Domestik PP',
                'deskripsi': 'Tiket pulang-pergi rute domestik Indonesia',
                'penyedia': 'Garuda Indonesia',
                'tipe_penyedia': 'airline',
                'miles': 15000,
                'valid_start': '2024-01-01',
                'program_end': '2025-12-31',
            },
            {
                'kode': 'RWD-002',
                'nama': 'Upgrade ke Business Class',
                'deskripsi': 'Upgrade dari economy class ke business class',
                'penyedia': 'Garuda Indonesia',
                'tipe_penyedia': 'airline',
                'miles': 25000,
                'valid_start': '2024-01-01',
                'program_end': '2025-12-31',
            },
            {
                'kode': 'RWD-003',
                'nama': 'Voucher Hotel Rp 500.000',
                'deskripsi': 'Voucher hotel Jabodetabek',
                'penyedia': 'TravelokaPartner',
                'tipe_penyedia': 'partner',
                'miles': 8000,
                'valid_start': '2024-06-01',
                'program_end': '2025-06-30',
            },
            {
                'kode': 'RWD-004',
                'nama': 'Akses Lounge 1x',
                'deskripsi': 'Akses lounge seluruh bandara internasional',
                'penyedia': 'Plaza Premium',
                'tipe_penyedia': 'partner',
                'miles': 3000,
                'valid_start': '2024-01-01',
                'program_end': '2025-12-31',
            }
        ]
    }
    return render(request, 'members/kelola_hadiah.html', context)


def kelola_mitra(request):
    context = {
        'role': 'Staff',
        'nama': 'Mr. Admin Aero',
        'mitra_list': [
            {
                'email': 'partner@traveloka.com',
                'id_penyedia': 'PYD-001',
                'nama_mitra': 'TravelokaPartner',
                'tanggal_kerja_sama': '2023-01-15'
            },
            {
                'email': 'partner@plazapremium.com',
                'id_penyedia': 'PYD-002',
                'nama_mitra': 'Plaza Premium',
                'tanggal_kerja_sama': '2023-06-01'
            }
        ]
    }
    return render(request, 'members/kelola_mitra.html', context)