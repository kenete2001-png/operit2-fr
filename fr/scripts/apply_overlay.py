#!/usr/bin/env python3
"""Applique l'édition française sur une copie du code officiel.
- Copie les ressources françaises (jamais écrasées par upstream : elles n'existent pas chez lui).
- Applique les correctifs fr/patches/patches.json par remplacement exact.
- Idempotent. Échoue (code 2) si un correctif ne s'applique plus : upstream a changé ce code.
"""
import json, os, shutil, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def p(*a): return os.path.join(ROOT, *a)
# Le français officiel (upstream) prime : on ne fait que compléter les clés absentes
# avec nos traductions, et remplacer une valeur restée en chinois.
import re
dst = p('apps','flutter','app','lib','l10n','app_fr.arb')
ours = json.load(open(p('fr','l10n','app_fr.arb'), encoding='utf-8'))
if os.path.exists(dst):
    theirs = json.load(open(dst, encoding='utf-8'))
    en = json.load(open(p('apps','flutter','app','lib','l10n','app_en.arb'), encoding='utf-8'))
    added = 0
    for k, v in en.items():
        if k.startswith('@'):
            continue
        cur = theirs.get(k)
        if cur is None or (isinstance(cur, str) and re.search(r'[\u4e00-\u9fff]', cur)):
            theirs[k] = ours.get(k, v); added += 1
    json.dump(theirs, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'ARB    français officiel conservé, {added} clé(s) complétée(s)')
else:
    shutil.copy(p('fr','l10n','app_fr.arb'), dst)
os.makedirs(p('apps','flutter','app','android','app','src','main','res','values-fr'), exist_ok=True)
shutil.copy(p('fr','android','values-fr','strings.xml'), p('apps','flutter','app','android','app','src','main','res','values-fr','strings.xml'))
failed = []
for patch in json.load(open(p('fr','patches','patches.json'), encoding='utf-8')):
    path = p(patch['file'])
    if not os.path.exists(path):
        failed.append((patch['id'], 'fichier absent')); continue
    text = open(path, encoding='utf-8').read()
    if patch['find'] in text:
        text = text.replace(patch['find'], patch['replace']) if patch.get('all') else text.replace(patch['find'], patch['replace'], 1)
        open(path, 'w', encoding='utf-8').write(text)
        print('OK     ', patch['id'])
    elif patch['replace'] in text:
        print('DÉJÀ   ', patch['id'])
    else:
        failed.append((patch['id'], 'texte d\'origine introuvable'))
for pid, why in failed: print('ÉCHEC  ', pid, '-', why)
sys.exit(2 if failed else 0)
