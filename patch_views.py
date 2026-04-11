import os
import re

files_to_patch = [
    'people/views.py',
    'academics/views.py',
    'attendance/views.py',
    'grading/views.py',
    'fees/views.py',
    'certificates/views.py',
    'ai_assistant/views.py',
]

pattern = re.compile(
    r'@login_required\s*\n\s*def index\(request\):\s*\n\s*if request\.user\.role != [\'"]ADMIN[\'"]:\s*\n\s*messages\.error\(request, [\'"].*?[\'"]\)\s*\n\s*return redirect\([\'"]accounts:dashboard[\'"]\)',
    re.MULTILINE | re.DOTALL
)

replacement = """def index(request):
    if not request.user.is_authenticated or request.user.role != 'ADMIN':
        from django.contrib import messages
        messages.error(request, "You are not authorized to visit this page.")
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return redirect('school_index')"""

for filepath in files_to_patch:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = pattern.sub(replacement, content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Patched {filepath}')
        else:
            print(f'No change needed or pattern not matched for {filepath}')
