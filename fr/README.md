# Operit 2 Français

Édition française indépendante d'[Operit 2](https://github.com/AAswordman/Operit2).
Toutes les fonctionnalités officielles sont conservées : seule la langue change.

- Nom : **Operit 2 Français** — paquet Android : `app.operit.fr`
- S'installe **à côté** de l'application officielle (`app.operit`), données séparées.
- Signature propre et stable : les mises à jour de l'édition française s'installent par-dessus sans perte.

## Installer
1. Ouvrir l'onglet **Releases** du dépôt, télécharger le dernier `Operit2-Francais-…-arm64.apk`.
2. L'ouvrir sur le téléphone et autoriser l'installation.
3. Pour revenir en arrière : réinstaller l'APK d'une Release précédente (désinstaller d'abord si Android refuse une version plus ancienne ; faire une sauvegarde avant).

## Comment c'est organisé
| Élément | Rôle |
|---|---|
| branche `upstream` | copie exacte du dépôt officiel, jamais modifiée |
| branche `fr` | code officiel **non modifié** + dossier `fr/` + workflows |
| `fr/l10n/app_fr.arb` | toutes les traductions de l'interface |
| `fr/android/values-fr/` | textes Android (raccourcis, service) |
| `fr/patches/patches.json` | les quelques correctifs (identité, français par défaut, repli anglais pour les extensions) |
| `fr/scripts/apply_overlay.py` | applique le tout **au moment de la compilation** |
| `fr/scripts/check_translations.py` | rapport : clés manquantes, chinois restant |

Le code officiel n'est jamais modifié dans la branche `fr` : la fusion d'une nouvelle version officielle ne peut donc pas écraser les traductions.

## Mises à jour automatiques
Chaque lundi (ou à la demande : onglet Actions → « Synchro officielle » → Run workflow) :
1. le dépôt officiel est copié dans `upstream` puis fusionné dans `fr` (un tag `avant-synchro-AAAAMMJJ` est posé avant) ;
2. les correctifs et traductions sont testés sur le nouveau code ;
3. si un correctif ne s'applique plus, ou si de nouveaux textes sont à traduire, un **ticket** est ouvert avec la liste ;
4. sinon l'APK est compilé, signé et publié dans une nouvelle Release.

Un texte nouveau pas encore traduit s'affiche en **anglais**, jamais en chinois.

## Ajouter / corriger une traduction
Modifier `fr/l10n/app_fr.arb` (clé → texte), garder les `{variables}` intactes, puis lancer « Build APK » dans Actions.

## Retour arrière
- Code : `git reset --hard avant-synchro-AAAAMMJJ` sur la branche `fr`.
- Application : chaque Release garde son APK.

## Limites connues (à traiter dans les prochaines étapes)
- Textes chinois écrits directement dans le code (hors système de traduction) : affichés en anglais ou chinois selon l'écran, francisation progressive.
- Extensions : affichées en anglais tant que leur catalogue français n'existe pas.
- Prompts système envoyés à l'IA : volontairement non traduits.
- Fournisseur d'accessibilité séparé (`app.operit.accessibility`) : signé par l'officiel, l'automatisation d'interface nécessitera une version française dédiée.
