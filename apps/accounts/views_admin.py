from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm # We need to ensure we have a form for this

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    wrap.__doc__ = function.__doc__
    return wrap

@login_required
@admin_required
def user_list(request, role):
    users = CustomUser.objects.filter(role=role).select_related('kelas')
    role_label = role.capitalize()
    return render(request, 'accounts/admin/user_list.html', {'users': users, 'role': role, 'role_label': role_label})

@login_required
@admin_required
def user_create(request, role):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role # Force role
            user.save()
            form.save_m2m() # Save ManyToMany (ampu_mapel)
            messages.success(request, f'{role.capitalize()} berhasil ditambahkan.')
            return redirect('user_list', role=role)
    else:
        form = CustomUserCreationForm(initial={'role': role})
        
    return render(request, 'accounts/admin/user_form.html', {
        'form': form,
        'role': role,
        'role_label': role.capitalize()
    })

@login_required
@admin_required
def user_edit(request, role, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            # Ensure role doesn't change implicitly if we don't want it to
            user.role = role 
            user.save()
            form.save_m2m()
            messages.success(request, f'Data {role} berhasil diperbarui.')
            return redirect('user_list', role=role)
    else:
        form = CustomUserCreationForm(instance=user)
        # We don't want to show the hash in password field
        form.fields['password'].widget.attrs['placeholder'] = "Isi hanya jika ingin mengubah password"
        form.fields['password'].required = False

    return render(request, 'accounts/admin/user_form.html', {
        'form': form,
        'role': role,
        'role_label': role.capitalize(),
        'target_user': user
    })

@login_required
@admin_required
def user_delete(request, role, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User berhasil dihapus.')
        return redirect('user_list', role=role)
    return redirect('user_list', role=role)

# ... existing imports ...
import openpyxl
from django.http import HttpResponse
from .services import UserImportService

@login_required
@admin_required
def download_template_user(request, role):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=template_import_{role}.xlsx'
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Template {role.capitalize()}"
    
    # Headers
    headers = ['Username', 'Nama Lengkap', 'Password (Default: 123456)']
    if role == 'siswa':
        headers.extend(['NISN', 'Nama Kelas (Persis)'])
    elif role == 'guru':
        headers.extend(['NIP (Opsional)'])
        
    ws.append(headers)
    
    # Example Row
    example = ['siswa01', 'Ahmad Siswa', 'rahasia123']
    if role == 'siswa':
        example.extend(['1234567890', 'X IPA 1'])
    elif role == 'guru':
        example.extend(['19800101...'])
        
    ws.append(example)
    
    wb.save(response)
    return response

@login_required
@admin_required
def import_user(request, role):
    if request.method == 'POST':
        if 'file' in request.FILES:
            excel_file = request.FILES['file']
            service = UserImportService(excel_file)
            valid_data, errors = service.parse(role=role)
            
            if errors:
                for err in errors:
                    messages.error(request, err)
                # Still show preview if needed, or just redirect back
                return render(request, 'accounts/admin/import_user.html', {
                    'role': role,
                    'errors': errors,
                    'preview_data': valid_data
                })
            
            # If confirmed (simple flow: direct commit if no errors, or add preview step?)
            # Let's do: If VALID and NO ERRORS -> Save automatically? 
            # Or Show Preview first? User asked for "Preview" in previous tasks.
            # Let's do PREVIEW STEP if POST has file, COMMIT STEP if POST has 'confirm'.
            
            # Using Session to store temp data is heavy. 
            # Let's simplify: 
            # 1. Upload -> Parse -> Show Result Table (Valid & Error)
            # 2. If all valid -> Show "Commit" button hidden input filename? No, can't re-upload easily.
            # 3. Best: Parse -> If Warnings, show them. If "Confirm" clicked, save.
            
            # Current simplified approach:
            # If valid > 0 and errors == 0: Save immediately? 
            # Or Preview Page? Let's use PREVIEW Page pattern.
            
            request.session[f'import_{role}_data'] = valid_data # Store parsed data in session
            return render(request, 'accounts/admin/import_preview.html', {
                'role': role,
                'valid_data': valid_data,
                'errors': errors
            })
            
        elif 'confirm' in request.POST:
            # Commit from session
            valid_data = request.session.get(f'import_{role}_data', [])
            if not valid_data:
                messages.error(request, "Data import kadaluarsa or kosong.")
                return redirect('import_user', role=role)
            
            # Re-instantiate service (dummy) just to use save logic or static method?
            # Creating a lightweight helper or just code it here
            service = UserImportService()
            service.valid_data = valid_data
            count = service.save_users()
            
            del request.session[f'import_{role}_data']
            messages.success(request, f"Sukses mengimport {count} {role}.")
            return redirect('user_list', role=role)

    return render(request, 'accounts/admin/import_user.html', {'role': role})
