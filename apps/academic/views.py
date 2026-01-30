from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MataPelajaran, Kelas, Jurusan
from .forms import MataPelajaranForm, KelasForm, JurusanForm

# Helper decorator for Admin check
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    wrap.__doc__ = function.__doc__
    return wrap

# --- MATA PELAJARAN ---

@login_required
def mapel_list(request):
    if request.user.role not in ['guru', 'admin']:
        return redirect('login')
    mapel_list = MataPelajaran.objects.all()
    return render(request, 'academic/mapel_list.html', {'mapel_list': mapel_list})

@login_required
def mapel_create(request):
    if request.user.role not in ['guru', 'admin']:
        return redirect('login')
    
    if request.method == 'POST':
        form = MataPelajaranForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mata Pelajaran berhasil ditambahkan.')
            return redirect('mapel_list')
    else:
        form = MataPelajaranForm()
    return render(request, 'academic/mapel_form.html', {'form': form, 'title': 'Tambah Mata Pelajaran'})

@login_required
def mapel_edit(request, pk):
    if request.user.role not in ['guru', 'admin']:
        return redirect('login')
        
    mapel = get_object_or_404(MataPelajaran, pk=pk)
    if request.method == 'POST':
        form = MataPelajaranForm(request.POST, instance=mapel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mata Pelajaran berhasil diperbarui.')
            return redirect('mapel_list')
    else:
        form = MataPelajaranForm(instance=mapel)
    return render(request, 'academic/mapel_form.html', {'form': form, 'title': 'Edit Mata Pelajaran'})

@login_required
def mapel_delete(request, pk):
    if request.user.role not in ['guru', 'admin']:
        return redirect('login')
    
    mapel = get_object_or_404(MataPelajaran, pk=pk)
    if request.method == 'POST':
        mapel.delete()
        messages.success(request, 'Mata Pelajaran berhasil dihapus.')
        return redirect('mapel_list')
    return render(request, 'academic/mapel_confirm_delete.html', {'mapel': mapel})

# --- KELAS (Admin Only) ---

@login_required
def kelas_list(request):
    if request.user.role not in ['admin', 'guru', 'proktor']:
        return redirect('login')
    kelas_list = Kelas.objects.select_related('jurusan').all().order_by('tingkat', 'nama')
    return render(request, 'academic/kelas_list.html', {'kelas_list': kelas_list})

@login_required
def kelas_create(request):
    if request.user.role != 'admin': return redirect('login')
    if request.method == 'POST':
        form = KelasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kelas berhasil ditambahkan.')
            return redirect('kelas_list')
    else:
        form = KelasForm()
    return render(request, 'academic/kelas_form.html', {'form': form, 'title': 'Tambah Kelas'})

@login_required
def kelas_edit(request, pk):
    if request.user.role != 'admin': return redirect('login')
    kelas = get_object_or_404(Kelas, pk=pk)
    if request.method == 'POST':
        form = KelasForm(request.POST, instance=kelas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kelas berhasil diperbarui.')
            return redirect('kelas_list')
    else:
        form = KelasForm(instance=kelas)
    return render(request, 'academic/kelas_form.html', {'form': form, 'title': 'Edit Kelas'})

@login_required
def kelas_delete(request, pk):
    if request.user.role != 'admin': return redirect('login')
    kelas = get_object_or_404(Kelas, pk=pk)
    if request.method == 'POST':
        kelas.delete()
        messages.success(request, 'Kelas berhasil dihapus.')
        return redirect('kelas_list')
    return render(request, 'academic/kelas_confirm_delete.html', {'object': kelas, 'type': 'Kelas'})

# --- JURUSAN (Admin Only) ---

@login_required
def jurusan_list(request):
    if request.user.role != 'admin': return redirect('login')
    jurusan_list = Jurusan.objects.all()
    return render(request, 'academic/jurusan_list.html', {'jurusan_list': jurusan_list})

@login_required
def jurusan_create(request):
    if request.user.role != 'admin': return redirect('login')
    if request.method == 'POST':
        form = JurusanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jurusan berhasil ditambahkan.')
            return redirect('jurusan_list')
    else:
        form = JurusanForm()
    return render(request, 'academic/jurusan_form.html', {'form': form, 'title': 'Tambah Jurusan'})

@login_required
def jurusan_edit(request, pk):
    if request.user.role != 'admin': return redirect('login')
    jurusan = get_object_or_404(Jurusan, pk=pk)
    if request.method == 'POST':
        form = JurusanForm(request.POST, instance=jurusan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jurusan berhasil diperbarui.')
            return redirect('jurusan_list')
    else:
        form = JurusanForm(instance=jurusan)
    return render(request, 'academic/jurusan_form.html', {'form': form, 'title': 'Edit Jurusan'})

@login_required
def jurusan_delete(request, pk):
    if request.user.role != 'admin': return redirect('login')
    jurusan = get_object_or_404(Jurusan, pk=pk)
    if request.method == 'POST':
        jurusan.delete()
        messages.success(request, 'Jurusan berhasil dihapus.')
        return redirect('jurusan_list')
    return render(request, 'academic/jurusan_confirm_delete.html', {'object': jurusan, 'type': 'Jurusan'})

@login_required
def cetak_kartu_kelas(request, pk):
    """
    Generate participant cards for all students in a specific class.
    Universal/Global card (not tied to specific exam).
    Accessible by: Admin, Proktor, Guru
    """
    if request.user.role not in ['admin', 'proktor', 'guru']:
        return redirect('login')

    kelas = get_object_or_404(Kelas, pk=pk)
    
    # Get all students in this class
    peserta_list = kelas.siswa_set.all().order_by('nama', 'username')
    
    return render(request, 'academic/kartu_peserta_kelas.html', {
        'kelas': kelas,
        'peserta_list': peserta_list
    })
