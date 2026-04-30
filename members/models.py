from django.db import models

class Member(models.Model):
    nama = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[('Staff', 'Staff'), ('Member', 'Member')])

    def __str__(self):
        return self.nama

class Klaim(models.Model):
    STATUS_CHOICES = [
        ('Menunggu', 'Menunggu'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    maskapai = models.CharField(max_length=100)
    bandara_asal = models.CharField(max_length=10)  # IATA code
    bandara_tujuan = models.CharField(max_length=10)  # IATA code
    tanggal_penerbangan = models.DateField()
    flight_number = models.CharField(max_length=20)
    nomor_tiket = models.CharField(max_length=20)
    kelas_kabin = models.CharField(max_length=20, choices=[
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First', 'First'),
    ])
    pnr = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Menunggu')
    timestamp_pengajuan = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('flight_number', 'tanggal_penerbangan', 'nomor_tiket')

    def __str__(self):
        return f"Klaim {self.id} - {self.member.nama}"
