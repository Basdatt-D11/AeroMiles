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


def login_register(request):
    """Halaman login dan registrasi (frontend only)"""
    return render(request, 'members/login_register.html')


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


# Klaim views for Member
def ajukan_klaim(request):
    member = Member.objects.filter(role='Member').first()  # Hardcode for demo
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
    return render(request, 'members/ajukan_klaim.html', context)


def riwayat_klaim(request):
    member = Member.objects.filter(role='Member').first()
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
    return render(request, 'members/riwayat_klaim.html', context)


def edit_klaim(request, klaim_id):
    member = Member.objects.filter(role='Member').first()
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
    return render(request, 'members/edit_klaim.html', context)


def batalkan_klaim(request, klaim_id):
    member = Member.objects.filter(role='Member').first()
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
    return render(request, 'members/batalkan_klaim.html', context)


# Klaim views for Staff
def kelola_klaim(request):
    klaims = Klaim.objects.all().order_by('-timestamp_pengajuan')
    context = {
        'role': 'Staff',
        'nama': 'Mr. John William Doe',
        'klaims': klaims,
    }
    return render(request, 'members/kelola_klaim.html', context)


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