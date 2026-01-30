from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting login for user: {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Login successful for: {username}, Role: {user.role}")
            login(request, user)
            return redirect_based_on_role(user)
        else:
            print(f"Login failed for: {username}")
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def redirect_based_on_role(user):
    if user.is_superuser:
        return redirect('admin_dashboard')
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'guru':
        return redirect('guru_dashboard')
    elif user.role == 'siswa':
        return redirect('siswa_dashboard')
    elif user.role == 'proktor':
        return redirect('proktor_dashboard')
    elif user.role == 'waka':
        return redirect('waka_dashboard')
    else:
        return redirect('login')

from apps.accounts.models import CustomUser
from apps.exams.models import Ujian, BankSoal

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('login')
        
    from apps.exams.models import SesiUjian
    
    # Global Stats
    total_siswa_mengerjakan = SesiUjian.objects.filter(is_finished=False).count()
    total_siswa_selesai = SesiUjian.objects.filter(is_finished=True).count()
    ujian_aktif = Ujian.objects.filter(aktif=True)
    
    # Build monitoring data per exam for Admin (Global View)
    monitoring_data = []
    for ujian in ujian_aktif:
        sesi_aktif = SesiUjian.objects.filter(ujian=ujian, is_finished=False).count()
        sesi_selesai = SesiUjian.objects.filter(ujian=ujian, is_finished=True).count()
        total_peserta = CustomUser.objects.filter(role='siswa', kelas__ujian=ujian).count()
        
        monitoring_data.append({
            'ujian': ujian,
            'aktif': sesi_aktif,
            'selesai': sesi_selesai,
            'total_peserta': total_peserta
        })

    context = {
        'total_siswa': CustomUser.objects.filter(role='siswa').count(),
        'total_guru': CustomUser.objects.filter(role='guru').count(),
        'active_exams': ujian_aktif.count(),
        'total_bank_soal': BankSoal.objects.count(),
        'total_siswa_mengerjakan': total_siswa_mengerjakan,
        'total_siswa_selesai': total_siswa_selesai,
        'monitoring_data': monitoring_data,
        'ujian_aktif_list': ujian_aktif, # To avoid conflict with int count
    }
    return render(request, 'dashboard/admin.html', context)

@login_required
def guru_dashboard(request):
    if request.user.role != 'guru':
        return redirect('login')
        
    from apps.exams.models import SesiUjian, JadwalPengawas
    
    # Get stats
    bank_soal_list = BankSoal.objects.filter(guru=request.user).order_by('-created_at')
    ujian_list = Ujian.objects.filter(bank_soal__guru=request.user).order_by('-waktu_mulai')
    
    active_exams_list = Ujian.objects.filter(bank_soal__guru=request.user, aktif=True)
    
    # Get exams where this teacher is assigned as supervisor
    supervisor_assignments = JadwalPengawas.objects.filter(proktor=request.user).select_related('ujian', 'kelas').order_by('-ujian__waktu_mulai')
    
    # Build monitoring data for this teacher's active exams (Created by them)
    monitoring_data = []
    for ujian in active_exams_list:
        sesi_aktif = SesiUjian.objects.filter(ujian=ujian, is_finished=False).count()
        sesi_selesai = SesiUjian.objects.filter(ujian=ujian, is_finished=True).count()
        total_peserta = CustomUser.objects.filter(role='siswa', kelas__ujian=ujian).count()
        
        monitoring_data.append({
            'ujian': ujian,
            'aktif': sesi_aktif,
            'selesai': sesi_selesai,
            'total_peserta': total_peserta
        })

    context = {
        'bank_soal_list': bank_soal_list,
        'ujian_list': ujian_list,
        'supervisor_assignments': supervisor_assignments,
        'total_bank_soal': bank_soal_list.count(),
        'total_ujian': ujian_list.count(),
        'active_exams': active_exams_list.count(),
        'monitoring_data': monitoring_data,
    }
    return render(request, 'dashboard/guru.html', context)

from apps.exams.models import Ujian
from django.utils import timezone

@login_required
def siswa_dashboard(request):
    user = request.user
    if user.role != 'siswa':
        return redirect('login')
    
    active_exams = []
    if user.kelas:
        now = timezone.now()
        # Fetch exams
        exams_qs = Ujian.objects.filter(
            kelas=user.kelas,
            aktif=True,
            waktu_mulai__lte=now
        ).order_by('waktu_mulai').select_related('bank_soal', 'bank_soal__mapel')
        
        # Check status for each exam
        from apps.exams.models import SesiUjian
        active_exams = []
        for exam in exams_qs:
            sesi = SesiUjian.objects.filter(ujian=exam, siswa=user).first()
            exam_status = {
                'obj': exam,
                'is_finished': sesi.is_finished if sesi else False,
                'has_started': True if sesi else False
            }
            active_exams.append(exam_status)

    return render(request, 'dashboard/siswa.html', {'exams': active_exams})

@login_required
def waka_dashboard(request):
    if request.user.role != 'waka':
        return redirect('login')
    
    from apps.exams.models import SesiUjian
    from django.db.models import Avg, Count
    
    # Statistics for Waka
    context = {
        'total_ujian': Ujian.objects.count(),
        'ujian_aktif': Ujian.objects.filter(aktif=True).count(),
        'total_siswa': CustomUser.objects.filter(role='siswa').count(),
        'total_guru': CustomUser.objects.filter(role='guru').count(),
        'total_sesi': SesiUjian.objects.filter(is_finished=True).count(),
        'rata_nilai': SesiUjian.objects.filter(is_finished=True, status='GRADED').aggregate(Avg('nilai'))['nilai__avg'] or 0,
        'recent_exams': Ujian.objects.order_by('-waktu_mulai')[:10],
    }
    return render(request, 'dashboard/waka.html', context)

@login_required
def proktor_dashboard(request):
    if request.user.role != 'proktor':
        return redirect('login')
    
    from apps.exams.models import SesiUjian
    from django.utils import timezone
    
    now = timezone.now()
    
    # Get all active exams assigned to this proctor OR all (if logic desires, but we want granular)
    # Logic: Only show exams where this proctor is assigned in at least one class
    from apps.exams.models import JadwalPengawas
    
    assignments = JadwalPengawas.objects.filter(proktor=request.user, ujian__aktif=True).select_related('ujian', 'kelas')
    # Group by Exam because one proctor might oversee multiple classes in same exam (unlikely but possible)
    # or just list distinct exams
    
    assigned_exam_ids = assignments.values_list('ujian_id', flat=True)
    ujian_aktif = Ujian.objects.filter(id__in=assigned_exam_ids, aktif=True)
    
    # Stats for proktor (Filtered by assigned classes)
    # We need to filter sessions where siswa.kelas is in the assigned classes for that exam
    
    total_siswa_mengerjakan = 0
    total_siswa_selesai = 0
    
    # Simple global stats for dashboard cards (Sum of all assigned responsibilities)
    for assignment in assignments:
        total_siswa_mengerjakan += SesiUjian.objects.filter(
            ujian=assignment.ujian, 
            siswa__kelas=assignment.kelas, 
            is_finished=False
        ).count()
        total_siswa_selesai += SesiUjian.objects.filter(
            ujian=assignment.ujian, 
            siswa__kelas=assignment.kelas, 
            is_finished=True
        ).count()
    
    # Build monitoring data per exam
    monitoring_data = []
    for ujian in ujian_aktif:
        # Which classes are assigned to ME for THIS exam?
        my_classes = assignments.filter(ujian=ujian).values_list('kelas', flat=True)
        
        sesi_aktif = SesiUjian.objects.filter(
            ujian=ujian, 
            siswa__kelas__in=my_classes,
            is_finished=False
        ).count()
        
        sesi_selesai = SesiUjian.objects.filter(
            ujian=ujian, 
            siswa__kelas__in=my_classes, 
            is_finished=True
        ).count()
        
        # Calculate total students in my assigned classes
        total_peserta = CustomUser.objects.filter(role='siswa', kelas__id__in=my_classes).count()
        
        monitoring_data.append({
            'ujian': ujian,
            'aktif': sesi_aktif,
            'selesai': sesi_selesai,
            'total_peserta': total_peserta
        })
    
    context = {
        'ujian_aktif': ujian_aktif,
        'total_siswa_mengerjakan': total_siswa_mengerjakan,
        'total_siswa_selesai': total_siswa_selesai,
        'monitoring_data': monitoring_data,
    }
    return render(request, 'dashboard/proktor.html', context)
