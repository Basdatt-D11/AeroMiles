from django.shortcuts import render

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

def redeem_list(request):
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

    context = {
        'role': 'Member',
        'nama': 'Mr. John Doe',
        'rewards': rewards,
        'history': history,
    }
    return render(request, 'members/redeem_list.html', context)


def buy_package(request):
    packages = [
        {'id': 'PKG-001', 'miles': 1000, 'price': 50000},
        {'id': 'PKG-002', 'miles': 5000, 'price': 200000},
        {'id': 'PKG-003', 'miles': 10000, 'price': 350000},
        {'id': 'PKG-004', 'miles': 25000, 'price': 800000},
    ]

    history = [
        {'id': 201, 'package_id': 'PKG-002', 'miles': 5000, 'price': 200000, 'date': '2026-02-15'},
    ]

    context = {
        'role': 'Member',
        'nama': 'Mr. John Doe',
        'packages': packages,
        'history': history,
    }
    return render(request, 'members/buy_package.html', context)


def tier_info(request):
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

    context = {
        'role': 'Member',
        'nama': 'Mr. John Doe',
        'current_miles': current_miles,
        'tiers': tiers,
        'current_tier': current_tier,
        'next_tier': next_tier,
        'miles_to_next': miles_to_next,
        'progress': progress,
    }
    return render(request, 'members/tier_info.html', context)


def transaction_report(request):
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

    context = {
        'role': 'Staff',
        'nama': 'Staff Admin',
        'transactions': transactions,
        'top_members': top_members,
    }
    return render(request, 'members/transaction_report.html', context)