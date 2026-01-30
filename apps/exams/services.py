import openpyxl
from .models import ButirSoal

class QuestionImportService:
    def __init__(self, file=None):
        if file:
            self.wb = openpyxl.load_workbook(file, data_only=True)
            self.sheet = self.wb.active
        else:
            self.wb = None
            self.sheet = None
        self.errors = []
        self.valid_data = []

    def parse(self):
        """
        Parses the Excel file and returns (valid_data, errors).
        """
        # Iterate from row 2 (skip header)
        for index, row in enumerate(self.sheet.iter_rows(min_row=2, values_only=True), start=2):
            # Check if row is empty
            if not any(row):
                continue
            
            # Expected schema:
            # 0: Pertanyaan
            # 1: Opsi A
            # 2: Opsi B
            # 3: Opsi C
            # 4: Opsi D
            # 5: Opsi E
            # 6: Kunci (A/B/C/D/E) OR Empty for Essay?
            # 7: Bobot
            # 8: Tipe (PG/ESSAY) -- New Optional Column

            pertanyaan = row[0]
            if not pertanyaan:
                self.errors.append(f"Row {index}: 'Pertanyaan' is required.")
                continue

            # Determine Type
            jenis_soal = 'PG'
            kunci = row[6]
            
            # Check explicit type column if exists (col 8)
            if len(row) > 8 and row[8]:
                raw_type = str(row[8]).upper().strip()
                if 'ESSAY' in raw_type or 'URAIAN' in raw_type:
                    jenis_soal = 'ESSAY'
            
            # Heuristic: If Kunci is empty/long text, might be essay?
            # But strictly, let's default to PG unless specified or inferred.
            
            opsi_a = row[1]
            opsi_b = row[2]
            
            # Validation for PG
            if jenis_soal == 'PG':
                if not kunci:
                    self.errors.append(f"Row {index}: PG Question requires 'Kunci Jawaban'.")
                else:
                    kunci = str(kunci).strip().upper()
                    if kunci not in ['A', 'B', 'C', 'D', 'E']:
                        self.errors.append(f"Row {index}: Invalid Kunci '{kunci}'. Must be A-E.")
                
                # if not opsi_a or not opsi_b:
                #    self.errors.append(f"Row {index}: PG requires at least Opsi A and B.")

            elif jenis_soal == 'ESSAY':
                # Essay validation
                pass

            if not self.errors:
                self.valid_data.append({
                    'index': index,
                    'pertanyaan': pertanyaan,
                    'opsi_a': row[1],
                    'opsi_b': row[2],
                    'opsi_c': row[3],
                    'opsi_d': row[4],
                    'opsi_e': row[5],
                    'kunci_jawaban': kunci if jenis_soal == 'PG' else None,
                    'bobot': row[7] if len(row) > 7 and row[7] else 1,
                    'jenis_soal': jenis_soal
                })

        return self.valid_data, self.errors

    def save_to_bank(self, bank, data_list):
        """
        Saves parsed data list to the database.
        """
        count = 0
        for data in data_list:
            ButirSoal.objects.create(
                bank_soal=bank,
                pertanyaan=data['pertanyaan'],
                jenis_soal=data['jenis_soal'],
                opsi_a=data['opsi_a'],
                opsi_b=data['opsi_b'],
                opsi_c=data['opsi_c'],
                opsi_d=data['opsi_d'],
                opsi_e=data['opsi_e'],
                kunci_jawaban=data['kunci_jawaban'],
                bobot=data['bobot']
            )
            count += 1
        return count
