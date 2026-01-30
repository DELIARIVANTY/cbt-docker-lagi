from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import MataPelajaran
from .forms import MataPelajaranForm

@login_required
@require_POST
def api_add_mapel(request):
    if request.user.role != 'guru':
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    mapel_id = request.POST.get('mapel_id')
    
    if not mapel_id:
        return JsonResponse({'status': 'error', 'message': 'Mata Pelajaran wajib dipilih.'}, status=400)
        
    try:
        mapel = MataPelajaran.objects.get(pk=mapel_id)
        
        # Automatically assign to the teacher
        request.user.ampu_mapel.add(mapel)
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Mata Pelajaran berhasil ditambahkan ke daftar ajar Anda.',
            'mapel': {'id': mapel.id, 'nama': mapel.nama}
        })
    except MataPelajaran.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Mata Pelajaran tidak ditemukan.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
