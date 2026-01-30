import re

# Read the template file
with open('templates/exams/lembar_ujian.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix pattern: <input ... value="X"\n ... class=... data-soal=... {% if\n ... saved.jawaban=='X' %}checked{% endif %}>
# Replace with single line version

# Pattern for radio buttons A-E
for letter in ['A', 'B', 'C', 'D', 'E']:
    pattern = (
        rf'<input type="radio" name="ans-\{{\{{ soal\.id \}}\}}" value="{letter}"\s*\n'
        rf'\s*class="form-selectgroup-input answer-input" data-soal="\{{\{{ soal\.id \}}\}}" \{{% if\s*\n'
        rf"\s*saved\.jawaban=='{letter}' %\}}checked\{{% endif %\}}>"
    )
    replacement = (
        f'<input type="radio" name="ans-{{{{ soal.id }}}}" value="{letter}" '
        f'class="form-selectgroup-input answer-input" data-soal="{{{{ soal.id }}}}" '
        f"{{% if saved.jawaban == '{letter}' %}}checked{{% endif %}}>"
    )
    content = re.sub(pattern, replacement, content)

# Fix checkbox pattern: <input type="checkbox" ... {% if saved.ragu_ragu %}checked{% endif\n ... %}>
pattern = (
    r'<input type="checkbox" class="btn-check ragu-check" id="raguCheck\{\{ soal\.id \}\}"\s*\n'
    r'\s*autocomplete="off" data-soal="\{\{ soal\.id \}\}" \{% if saved\.ragu_ragu %\}checked\{% endif\s*\n'
    r'\s*%\}>'
)
replacement = (
    '<input type="checkbox" class="btn-check ragu-check" id="raguCheck{{ soal.id }}" '
    'autocomplete="off" data-soal="{{ soal.id }}" {% if saved.ragu_ragu %}checked{% endif %}>'
)
content = re.sub(pattern, replacement, content)

# Write back
with open('templates/exams/lembar_ujian.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Template fixed successfully!")
print("Verifying...")

# Verify no broken tags remain
broken_patterns = [
    r'\{% if\s*\n\s*saved\.jawaban',
    r'\{% endif\s*\n\s*%\}'
]
for p in broken_patterns:
    if re.search(p, content):
        print(f"WARNING: Still found broken pattern: {p}")
    else:
        print(f"OK: Pattern {p[:30]}... not found")
