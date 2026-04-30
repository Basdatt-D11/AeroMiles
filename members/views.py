from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Member, Klaim
from django import forms

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
    return render(request, 'profile/profile_settings.html', context)


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
    return render(request, 'hadiah/kelola_hadiah.html', context)


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
    return render(request, 'mitra/kelola_mitra.html', context)
# Helper for mock member
def get_mock_member():
    member = Member.objects.filter(role='Member').first()
    if not member:
        member = Member.objects.create(role='Member', nama='Mr. John Doe', email='john@example.com', password='demo')
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
    member = get_mock_member()
    klaims = Klaim.objects.filter(member=member).order_by('-timestamp_pengajuan')
    status_filter = request.GET.get('status')
    if status_filter:
        klaims = klaims.filter(status=status_filter)
    context = {
        'role': 'Member',
        'nama': member.nama,
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
    klaims = Klaim.objects.all().order_by('-timestamp_pengajuan')
    context = {
        'role': 'Staff',
        'nama': 'Mr. John William Doe',
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
    rewards = [
        {
            'id': 1,
            'name': 'Voucher Makan Rp100.000',
            'description': 'Voucher restoran mitra senilai Rp100.000',
            'miles': 25000,
            'image': 'https://via.placeholder.com/120x80?text=Voucher'
        },
        {
            'id': 2,
            'name': 'Upgrade Kelas',
            'description': 'Upgrade ke kelas bisnis',
            'miles': 50000,
            'image': 'https://via.placeholder.com/120x80?text=Upgrade'
        }
    ]

    history = [
        {'id': 101, 'reward': 'Voucher Makan Rp100.000', 'miles': 25000, 'status': 'Sukses', 'date': '2026-04-10'},
        {'id': 102, 'reward': 'Upgrade Kelas', 'miles': 50000, 'status': 'Dibatalkan', 'date': '2026-03-12'},
    ]

    context = {'role': 'Member', 'nama': 'Mr. John Doe', 'rewards': rewards, 'history': history}
    return render(request, 'transactions/redeem_list.html', context)


def transactions_buy_package(request):
    packages = [
        {'id': 'PKG-001', 'miles': 1000, 'price': 50000},
        {'id': 'PKG-002', 'miles': 5000, 'price': 200000},
        {'id': 'PKG-003', 'miles': 10000, 'price': 350000},
        {'id': 'PKG-004', 'miles': 25000, 'price': 800000},
    ]
    history = [{'id': 201, 'package_id': 'PKG-002', 'miles': 5000, 'price': 200000, 'date': '2026-02-15'}]
    context = {'role': 'Member', 'nama': 'Mr. John Doe', 'packages': packages, 'history': history}
    return render(request, 'transactions/buy_package.html', context)


def transactions_transfer(request):
    history = [
        {'id': 301, 'to_email': 'alice@example.com', 'miles': 1500, 'date': '2026-04-20', 'status': 'Sukses'},
    ]
    context = {'role': 'Member', 'nama': 'Mr. John Doe', 'history': history}
    return render(request, 'transactions/transfer_miles.html', context)


def transactions_tier_info(request):
    current_miles = 42000
    tiers = [
        {'name': 'Blue', 'min_miles': 0, 'notes': ['Member awal'], 'color': 'secondary'},
        {'name': 'Silver', 'min_miles': 10000, 'notes': ['Minimal 2 penerbangan'], 'color': 'info'},
        {'name': 'Gold', 'min_miles': 30000, 'notes': ['Akses lounge', 'Prioritas boarding'], 'color': 'warning'},
        {'name': 'Platinum', 'min_miles': 60000, 'notes': ['Bonus miles 50%', 'Concierge'], 'color': 'primary'},
    ]
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
    context = {'role': 'Member', 'nama': 'Mr. John Doe', 'current_miles': current_miles, 'tiers': tiers, 'current_tier': current_tier, 'next_tier': next_tier, 'miles_to_next': miles_to_next, 'progress': progress}
    return render(request, 'transactions/tier_info.html', context)


def transactions_report(request):
    transactions = [
        {'id': 1, 'member': 'Alice', 'type': 'Redeem', 'amount': 0, 'miles': -25000, 'status': 'Sukses', 'timestamp': '2026-04-10 09:12'},
        {'id': 2, 'member': 'Bob', 'type': 'Transfer', 'amount': 0, 'miles': -5000, 'status': 'Sukses', 'timestamp': '2026-04-09 16:45'},
        {'id': 3, 'member': 'Charlie', 'type': 'Purchase', 'amount': 200000, 'miles': 5000, 'status': 'Pending', 'timestamp': '2026-04-08 11:20'},
        {'id': 4, 'member': 'Alice', 'type': 'Top-up', 'amount': 100000, 'miles': 1000, 'status': 'Sukses', 'timestamp': '2026-03-30 08:00'},
    ]
    top = {}
    for t in transactions:
        top.setdefault(t['member'], 0)
        top[t['member']] += t.get('miles', 0)
    top_members = sorted([{'member': k, 'total_miles': v} for k, v in top.items()], key=lambda x: x['total_miles'], reverse=True)
    context = {'role': 'Staff', 'nama': 'Staff Admin', 'transactions': transactions, 'top_members': top_members}
    return render(request, 'transactions/transaction_report.html', context)
