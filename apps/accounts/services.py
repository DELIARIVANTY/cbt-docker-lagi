import openpyxl
from .models import CustomUser
from apps.academic.models import Kelas

class UserImportService:
    def __init__(self, file=None):
        if file:
            self.wb = openpyxl.load_workbook(file, data_only=True)
            self.sheet = self.wb.active
        else:
            self.wb = None
            self.sheet = None
        self.errors = []
        self.valid_data = []

    def parse(self, role='siswa'):
        """
        Parses Excel for specific role.
        Rows: [Username, Nama, Password, NISN/NIP, Kelas(For Siswa)]
        """
        for index, row in enumerate(self.sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row): continue
            
            # Basic validation
            username = str(row[0]).strip() if row[0] else None
            nama = str(row[1]).strip() if len(row) > 1 and row[1] else None
            password = str(row[2]).strip() if len(row) > 2 and row[2] else "123456" # Default pass
            
            if not username:
                self.errors.append(f"Row {index}: Username required.")
                continue
                
            if CustomUser.objects.filter(username=username).exists():
                self.errors.append(f"Row {index}: Username '{username}' already exists.")
                continue

            extra_data = {}
            
            if role == 'siswa':
                nisn = str(row[3]).strip() if len(row) > 3 and row[3] else None
                kelas_nama = str(row[4]).strip() if len(row) > 4 and row[4] else None
                
                if not kelas_nama:
                    self.errors.append(f"Row {index}: Kelas wajib diisi untuk Siswa.")
                else:
                    # Find kelas
                    try:
                        # Loose match case insensitive
                        kelas_obj = Kelas.objects.filter(nama__iexact=kelas_nama).first()
                        if not kelas_obj:
                             self.errors.append(f"Row {index}: Kelas '{kelas_nama}' tidak ditemukan.")
                        else:
                            extra_data['kelas_id'] = kelas_obj.id # Store ID for serialization
                            extra_data['kelas_nama'] = kelas_obj.nama # For display
                            extra_data['nisn'] = nisn
                    except:
                         self.errors.append(f"Row {index}: Error lookup kelas.")
            
            # Identify row-specific errors before appending to valid_data
            # Actually, we should filter valid_data at the end or track per-row validity
            # For simplicity: If THIS row had error, don't append to valid_data
            row_clean = True
            for err in self.errors:
                if f"Row {index}:" in err: 
                    row_clean = False
                    break
            
            if row_clean:
                self.valid_data.append({
                    'username': username,
                    'nama': nama,
                    'password': password,
                    'role': role,
                    'extra': extra_data
                })
            
        return self.valid_data, self.errors

    def save_users(self):
        count = 0
        for item in self.valid_data:
            extra = item['extra']
            user = CustomUser.objects.create_user(
                username=item['username'],
                password=item['password'],
                role=item['role']
            )
            user.nama = item['nama']
            
            if item['role'] == 'siswa':
                user.nisn = extra.get('nisn')
                if extra.get('kelas_id'):
                    user.kelas_id = extra.get('kelas_id')
                
                
            user.save()
            count += 1
        return count
