import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Member, Klaim
from django import forms

def get_dummy_data():
    file_path = os.path.join(settings.BASE_DIR, 'dummy_data.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

MASKAPAI_CHOICES = [
    ('GA - Garuda Indonesia', 'GA - Garuda Indonesia'),
    ('SQ - Singapore Airlines', 'SQ - Singapore Airlines'),
    ('AA - American Airlines', 'AA - American Airlines'),
    ('EK - Emirates', 'EK - Emirates'),
]

BANDARA_CHOICES = [
    ('CGK', 'CGK - Soekarno-Hatta'),
    ('DPS', 'DPS - Ngurah Rai'),
    ('SIN', 'SIN - Changi'),
    ('NRT', 'NRT - Narita'),
    ('HND', 'HND - Haneda'),
]

KELAS_KABIN_CHOICES = [
    ('Economy', 'Economy'),
    ('Premium Economy', 'Premium Economy'),
    ('Business', 'Business'),
    ('First', 'First'),
]

class KlaimForm(forms.ModelForm):
    maskapai = forms.ChoiceField(choices=MASKAPAI_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    bandara_asal = forms.ChoiceField(choices=BANDARA_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    bandara_tujuan = forms.ChoiceField(choices=BANDARA_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    kelas_kabin = forms.ChoiceField(choices=KELAS_KABIN_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    tanggal_penerbangan = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    flight_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nomor_tiket = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    pnr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Klaim
        fields = ['maskapai', 'bandara_asal', 'bandara_tujuan', 'tanggal_penerbangan', 'flight_number', 'nomor_tiket', 'kelas_kabin', 'pnr']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def add_bootstrap_classes(self):
        for field in self.visible_fields():
            if field.field.widget.attrs.get('class') is None:
                field.field.widget.attrs['class'] = 'form-control'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()


def dashboard(request):
    data = get_dummy_data()
    user_email = request.session.get('user_email', 'john@example.com')
    user_role = request.session.get('user_role', 'Staff')
    
    user_info = {}
    if user_role == 'Member':
        user_info = next((m for m in data.get("MEMBER", []) if m['email'] == user_email), {})
        # Stats for member
        klaims = data.get("CLAIM_MISSING_MILES", [])
        user_info['klaim_menunggu'] = len([k for k in klaims if k.get('email_member') == user_email and k.get('status') == 'Menunggu'])
    else:
        user_info = next((s for s in data.get("STAF", []) if s['email'] == user_email), {})
        # Stats for staff
        klaims = data.get("CLAIM_MISSING_MILES", [])
        user_info['klaim_menunggu'] = len([k for k in klaims if k.get('status') == 'Menunggu'])
        user_info['klaim_disetujui'] = len([k for k in klaims if k.get('status') == 'Disetujui'])
        user_info['klaim_ditolak'] = len([k for k in klaims if k.get('status') == 'Ditolak'])

    context = {
        'nama': request.session.get('user_name', user_info.get('nama', 'User')),
        'email': user_email,
        'role': user_role,
        'user': user_info,
    }
    return render(request, 'members/dashboard.html', context)


def list_member(request):
    data = get_dummy_data()
    context = {
        'role': request.session.get('user_role', 'Staff'),
        'nama': request.session.get('user_name', 'Mr. John William Doe'),
        'member_list': data.get("MEMBER", [])
    }
    return render(request, 'members/list_member.html', context)


def list_identitas(request):
    data = get_dummy_data()
    identitas_list = data.get("IDENTITAS", [])
    # Filter for logged in user
    user_email = request.session.get('user_email', 'john@example.com')
    identitas_list = [i for i in identitas_list if i.get('email_member') == user_email]
    context = {
        'role': request.session.get('user_role', 'Member'),
        'nama': request.session.get('user_name', 'Mr. John Doe'),
        'identitas_list': identitas_list
    }
    return render(request, 'members/identitas.html', context)


def form_member(request):
    return render(request, 'members/form_member.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        data = get_dummy_data()
        users = data.get("PENGGUNA", [])
        
        user_match = next((u for u in users if u['email'] == email and u['password'] == password), None)
        
        if user_match:
            request.session['user_email'] = email
            request.session['user_role'] = user_match['role']
            
            # Find name from MEMBER or STAF
            name = "User"
            if user_match['role'] == 'Member':
                members = data.get("MEMBER", [])
                m = next((m for m in members if m['email'] == email), None)
                if m: name = m['nama']
                request.session['user_name'] = name
                return redirect('list_identitas')
            else:
                staff = data.get("STAF", [])
                s = next((s for s in staff if s['email'] == email), None)
                if s: name = s['nama']
                request.session['user_name'] = name
                return redirect('dashboard')
        else:
            messages.error(request, 'Email atau password salah.')
            
    context = {
        'demo_account': {
            'email': 'john@example.com',
            'password': 'password123',
            'role': 'Member',
        }
    }
    return render(request, 'members/login.html', context)


def logout_page(request):
    request.session.flush()
    return redirect('login_page')


def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        data = get_dummy_data()
        users = data.get("PENGGUNA", [])
        
        if any(u['email'] == email for u in users):
            messages.error(request, 'Email sudah terdaftar.')
        else:
            # Simulasi simpan (tidak benar-benar menulis ke JSON di sini agar tidak merusak data dummy asli)
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('login_page')
            
    return render(request, 'members/register.html')


def profile_settings(request):
    user_role = request.session.get('user_role', 'Member')
    user_email = request.session.get('user_email', 'john@example.com')
    user_name = request.session.get('user_name', 'User')
    
    # Split name for display
    name_parts = user_name.split(' ')
    first_name = name_parts[0] if len(name_parts) > 0 else "User"
    last_name = name_parts[-1] if len(name_parts) > 1 else ""
    
    context = {
        'role': user_role,
        'nama': user_name,
        'email': user_email,
        'nama_depan': first_name,
        'nama_belakang': last_name,
    }
    return render(request, 'profile/profile_settings.html', context)


def kelola_hadiah(request):
    data = get_dummy_data()
    context = {
        'role': request.session.get('user_role', 'Staff'),
        'nama': request.session.get('user_name', 'Mr. Admin Aero'),
        'hadiah_list': data.get("HADIAH", [])
    }
    return render(request, 'hadiah/kelola_hadiah.html', context)


def kelola_mitra(request):
    data = get_dummy_data()
    context = {
        'role': request.session.get('user_role', 'Staff'),
        'nama': request.session.get('user_name', 'Mr. Admin Aero'),
        'mitra_list': data.get("MITRA", [])
    }
    return render(request, 'mitra/kelola_mitra.html', context)
# Helper for mock member
def get_mock_member():
    member = Member.objects.filter(role='Member').first()
    if not member:
        member = Member.objects.create(role='Member', nama='Mr. John Doe')
    return member

# Klaim views for Member
def ajukan_klaim(request):
    member = get_mock_member()
    if request.method == 'POST':
        form = KlaimForm(request.POST)
        if form.is_valid():
            if Klaim.objects.filter(member=member, flight_number=form.cleaned_data['flight_number'], tanggal_penerbangan=form.cleaned_data['tanggal_penerbangan'], nomor_tiket=form.cleaned_data['nomor_tiket']).exists():
                form.add_error(None, 'Klaim untuk penerbangan ini sudah pernah diajukan.')
            else:
                klaim = form.save(commit=False)
                klaim.member = member
                klaim.save()
                messages.success(request, 'Klaim berhasil diajukan.')
                return redirect('riwayat_klaim')
    else:
        form = KlaimForm()
    context = {
        'role': 'Member',
        'nama': member.nama,
        'form': form,
    }
    return render(request, 'klaim/ajukan_klaim.html', context)


def riwayat_klaim(request):
    data = get_dummy_data()
    klaims = data.get("CLAIM_MISSING_MILES", [])
    
    # Filter for logged in user
    user_email = request.session.get('user_email', 'john@example.com')
    klaims = [k for k in klaims if k.get('email_member') == user_email]
    
    status_filter = request.GET.get('status')
    if status_filter:
        klaims = [k for k in klaims if k.get('status') == status_filter]
        
    context = {
        'role': request.session.get('user_role', 'Member'),
        'nama': request.session.get('user_name', 'Mr. John Doe'),
        'klaims': klaims,
        'form': KlaimForm(),
        'selected_status': status_filter,
    }
    return render(request, 'klaim/riwayat_klaim.html', context)


def edit_klaim(request, klaim_id):
    member = get_mock_member()
    klaim = get_object_or_404(Klaim, id=klaim_id, member=member, status='Menunggu')
    if request.method == 'POST':
        form = KlaimForm(request.POST, instance=klaim)
        if form.is_valid():
            if Klaim.objects.filter(member=member, flight_number=form.cleaned_data['flight_number'], tanggal_penerbangan=form.cleaned_data['tanggal_penerbangan'], nomor_tiket=form.cleaned_data['nomor_tiket']).exclude(pk=klaim.pk).exists():
                form.add_error(None, 'Klaim dengan data yang sama sudah ada.')
            else:
                form.save()
                messages.success(request, 'Klaim berhasil diupdate.')
                return redirect('riwayat_klaim')
    else:
        form = KlaimForm(instance=klaim)
    context = {
        'role': 'Member',
        'nama': member.nama,
        'form': form,
        'klaim': klaim,
    }
    return render(request, 'klaim/edit_klaim.html', context)


def batalkan_klaim(request, klaim_id):
    member = get_mock_member()
    klaim = get_object_or_404(Klaim, id=klaim_id, member=member, status='Menunggu')
    if request.method == 'POST':
        klaim.delete()
        messages.success(request, 'Klaim berhasil dibatalkan.')
        return redirect('riwayat_klaim')
    context = {
        'role': 'Member',
        'nama': member.nama,
        'klaim': klaim,
    }
    return render(request, 'klaim/batalkan_klaim.html', context)


# Klaim views for Staff
def kelola_klaim(request):
    data = get_dummy_data()
    klaims = data.get("CLAIM_MISSING_MILES", [])
    context = {
        'role': request.session.get('user_role', 'Staff'),
        'nama': request.session.get('user_name', 'Mr. John William Doe'),
        'klaims': klaims,
    }
    return render(request, 'klaim/kelola_klaim.html', context)


def approve_klaim(request, klaim_id):
    klaim = get_object_or_404(Klaim, id=klaim_id)
    klaim.status = 'Disetujui'
    klaim.save()
    messages.success(request, 'Klaim disetujui.')
    return redirect('kelola_klaim')


def reject_klaim(request, klaim_id):
    klaim = get_object_or_404(Klaim, id=klaim_id)
    klaim.status = 'Ditolak'
    klaim.save()
    messages.success(request, 'Klaim ditolak.')
    return redirect('kelola_klaim')


def transactions_redeem(request):
    data = get_dummy_data()
    user_email = request.session.get('user_email', 'john@example.com')
    history = data.get("REDEEM", [])
    # Filter for logged in user
    history = [h for h in history if h.get('email_member') == user_email]
    
    context = {
        'role': request.session.get('user_role', 'Member'),
        'nama': request.session.get('user_name', 'Mr. John Doe'),
        'rewards': data.get("HADIAH", []),
        'history': history
    }
    return render(request, 'transactions/redeem_list.html', context)


def transactions_buy_package(request):
    data = get_dummy_data()
    user_email = request.session.get('user_email', 'john@example.com')
    history = data.get("MEMBER_AWARD_MILES_PACKAGE", [])
    # Filter for logged in user
    history = [h for h in history if h.get('email_member') == user_email]
    
    context = {
        'role': request.session.get('user_role', 'Member'),
        'nama': request.session.get('user_name', 'Mr. John Doe'),
        'packages': data.get("AWARD_MILES_PACKAGE", []),
        'history': history
    }
    return render(request, 'transactions/buy_package.html', context)


def transactions_transfer(request):
    data = get_dummy_data()
    user_email = request.session.get('user_email', 'john@example.com')
    members = data.get("MEMBER", [])
    user_info = next((m for m in members if m['email'] == user_email), {})
    
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        amount = int(request.POST.get('amount', 0))
        note = request.POST.get('note', '')
        
        # Validations
        if recipient_email == user_email:
            messages.error(request, 'Anda tidak dapat mengirim miles ke diri sendiri.')
        elif amount > user_info.get('total_miles', 0):
            messages.error(request, 'Award miles Anda tidak mencukupi.')
        elif not any(m['email'] == recipient_email for m in members):
            messages.error(request, 'Email penerima tidak terdaftar sebagai member aktif.')
        else:
            # Simulate success (not writing to JSON to keep dummy clean)
            messages.success(request, f'Berhasil mentransfer {amount} miles ke {recipient_email}.')
            return redirect('transactions_transfer')

    transfers = data.get("TRANSFER", [])
    history = []
    for t in transfers:
        if t.get('sender') == user_email:
            # Type: Sent (Kirim)
            other_email = t.get('to_email')
            other_member = next((m for m in members if m['email'] == other_email), {'nama': 'Unknown'})
            history.append({
                'timestamp': t.get('date', '') + ' 10:30', # Mocking time
                'member_name': other_member.get('nama'),
                'member_email': other_email,
                'miles': t.get('miles', 0), # Positive value
                'note': t.get('catatan', '-'),
                'type': 'Kirim',
                'status': t.get('status', 'Sukses')
            })
        elif t.get('to_email') == user_email:
            # Type: Received (Terima)
            other_email = t.get('sender')
            other_member = next((m for m in members if m['email'] == other_email), {'nama': 'Unknown'})
            history.append({
                'timestamp': t.get('date', '') + ' 14:00', # Mocking time
                'member_name': other_member.get('nama'),
                'member_email': other_email,
                'miles': t.get('miles', 0), # Positive value
                'note': t.get('catatan', '-'),
                'type': 'Terima',
                'status': t.get('status', 'Sukses')
            })
    
    # Sort by timestamp
    history.sort(key=lambda x: x['timestamp'], reverse=True)

    context = {
        'role': request.session.get('user_role', 'Member'),
        'nama': request.session.get('user_name', user_info.get('nama', 'Mr. John Doe')),
        'email': user_email,
        'user': user_info,
        'history': history
    }
    return render(request, 'transactions/transfer_miles.html', context)


def transactions_tier_info(request):
    data = get_dummy_data()
    current_miles = 42000
    tiers = data.get("TIER", [])
    current_tier = tiers[0]
    for t in tiers:
        if current_miles >= t['min_miles']:
            current_tier = t
    next_tier = None
    for i, t in enumerate(tiers):
        if t['name'] == current_tier['name'] and i + 1 < len(tiers):
            next_tier = tiers[i+1]
            break
    if next_tier:
        miles_to_next = max(0, next_tier['min_miles'] - current_miles)
        range_start = current_tier['min_miles']
        range_end = next_tier['min_miles']
        progress = int(((current_miles - range_start) / (range_end - range_start)) * 100)
        progress = max(0, min(100, progress))
    else:
        miles_to_next = 0
        progress = 100
    context = {
        'role': request.session.get('user_role', 'Member'),
        'nama': request.session.get('user_name', 'Mr. John Doe'),
        'current_miles': current_miles,
        'tiers': tiers,
        'current_tier': current_tier,
        'next_tier': next_tier,
        'miles_to_next': miles_to_next,
        'progress': progress
    }
    return render(request, 'transactions/tier_info.html', context)


def transactions_report(request):
    data = get_dummy_data()
    transactions = []
    
    # Add from REDEEM
    for r in data.get("REDEEM", []):
        transactions.append({'id': r['id'], 'member': r['email_member'], 'type': 'Redeem', 'amount': 0, 'miles': -r['miles'], 'status': r['status'], 'timestamp': r['date']})
    # Add from TRANSFER
    for t in data.get("TRANSFER", []):
        transactions.append({'id': t['id'], 'member': t.get('sender', 'unknown'), 'type': 'Transfer', 'amount': 0, 'miles': -t['miles'], 'status': t['status'], 'timestamp': t['date']})
    # Add from MEMBER_AWARD_MILES_PACKAGE
    for p in data.get("MEMBER_AWARD_MILES_PACKAGE", []):
        transactions.append({'id': p['id'], 'member': p.get('email_member', 'unknown'), 'type': 'Purchase', 'amount': p['price'], 'miles': p['miles'], 'status': 'Sukses', 'timestamp': p['date']})
    
    # Sort by timestamp descending
    transactions.sort(key=lambda x: x['timestamp'], reverse=True)
    top = {}
    for t in transactions:
        top.setdefault(t['member'], 0)
        top[t['member']] += t.get('miles', 0)
    top_members = sorted([{'member': k, 'total_miles': v} for k, v in top.items()], key=lambda x: x['total_miles'], reverse=True)
    context = {
        'role': request.session.get('user_role', 'Staff'),
        'nama': request.session.get('user_name', 'Staff Admin'),
        'transactions': transactions,
        'top_members': top_members
    }
    return render(request, 'transactions/transaction_report.html', context)
