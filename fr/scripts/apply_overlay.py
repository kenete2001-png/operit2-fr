#!/usr/bin/env python3
"""Applique l'édition française sur une copie du code officiel.
- Copie les ressources françaises (jamais écrasées par upstream : elles n'existent pas chez lui).
- Applique les correctifs fr/patches/patches.json par remplacement exact.
- Idempotent. Échoue (code 2) si un correctif ne s'applique plus : upstream a changé ce code.
"""
import json, os, shutil, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def p(*a): return os.path.join(ROOT, *a)
shutil.copy(p('fr','l10n','app_fr.arb'), p('apps','flutter','app','lib','l10n','app_fr.arb'))
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
