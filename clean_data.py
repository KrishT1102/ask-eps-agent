import os

from pyparsing import line

os.makedirs('data/clean', exist_ok=True)

NOISE = ['skip to main','cookie','javascript','sign in',
        'facebook','twitter','instagram','powered by',
        'copyright','all rights reserved']


def clean_text(text):
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line: continue # skip empty
        if len(line) < 20: continue # skip menu items
        if any(n in line.lower() for n in NOISE): continue
        cleaned.append(line)
    return '\n'.join(cleaned)

for filename in os.listdir('data/raw'):
    if not filename.endswith('.txt'): continue
    with open(f'data/raw/{filename}', 'r', encoding='utf-8') as f:
        raw = f.read()
    clean = clean_text(raw)
    with open(f'data/clean/{filename}', 'w', encoding='utf-8') as f:
        f.write(clean)
    reduction = round((1 - len(clean)/len(raw)) * 100)
    print(f'{filename}: {reduction}% noise removed')
    
print('All files cleaned!')