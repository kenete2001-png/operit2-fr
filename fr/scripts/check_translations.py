#!/usr/bin/env python3
"""Rapport de traduction : clés manquantes, placeholders cassés, chinois restant.
Usage : check_translations.py [--strict]  (--strict : échoue si clé manquante ou chinois dans app_fr.arb)
"""
import json, os, re, sys, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CJK = re.compile(r'[\u4e00-\u9fff]')
en = json.load(open(os.path.join(ROOT,'apps/flutter/app/lib/l10n/app_en.arb'), encoding='utf-8'))
fr = json.load(open(os.path.join(ROOT,'fr/l10n/app_fr.arb'), encoding='utf-8'))
keys = [k for k in en if not k.startswith('@')]
missing = [k for k in keys if k not in fr]
obsolete = [k for k in fr if not k.startswith('@') and k not in en]
ph = re.compile(r'\{(\w+)[,}]')
broken = [k for k in keys if k in fr and set(ph.findall(en[k])) - {'count'} != set(ph.findall(fr[k])) - {'count'}]
cjk_fr = [k for k, v in fr.items() if isinstance(v, str) and CJK.search(v)]
# Chinois codé en dur dans le code de l'interface (hors commentaires)
lit = re.compile(r"""(['"])(?:(?!\1).)*[\u4e00-\u9fff](?:(?!\1).)*\1""")
hard = collections.Counter()
for base, ext in [('apps/flutter/app/lib','.dart'),('plugins/packages','.ts'),('plugins/packages','.mjs'),('core/crates','.rs')]:
    for r, ds, fs in os.walk(os.path.join(ROOT, base)):
        if 'generated' in r: continue
        for f in fs:
            if not f.endswith(ext): continue
            for line in open(os.path.join(r, f), encoding='utf-8', errors='ignore'):
                s = line.strip()
                if s.startswith(('//','*','/*','#')): continue
                if lit.search(s): hard[base] += 1
out = ['# Rapport de traduction', '',
       f'- Clés interface : {len(keys)}', f'- Traduites : {len(keys)-len(missing)}',
       f'- Manquantes (affichées en anglais) : {len(missing)}', f'- Obsolètes : {len(obsolete)}',
       f'- Placeholders à vérifier : {len(broken)}', f'- Chinois dans app_fr.arb : {len(cjk_fr)}', '',
       '## Chinois codé en dur restant (lignes)'] + [f'- {b} : {n}' for b, n in hard.items()]
if missing: out += ['', '## Clés à traduire'] + [f'- `{k}` : {en[k]}' for k in missing]
if broken: out += ['', '## Placeholders à vérifier'] + [f'- `{k}`' for k in broken]
os.makedirs(os.path.join(ROOT,'fr','reports'), exist_ok=True)
open(os.path.join(ROOT,'fr','reports','traduction.md'),'w',encoding='utf-8').write('\n'.join(out)+'\n')
print('\n'.join(out[:10]))
json.dump({'missing': missing}, open(os.path.join(ROOT,'fr','reports','missing.json'),'w'), ensure_ascii=False, indent=1)
if '--strict' in sys.argv and (cjk_fr or broken): sys.exit(1)
