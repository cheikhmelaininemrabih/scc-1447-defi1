# RCPSP Solver - Challenge S3C'1447

Ce projet propose une solution hybride **GANS (Genetic Algorithm + Neighborhood Search)** enrichie par **FBI (Forward-Backward Improvement)** pour résoudre le problème d'ordonnancement de projet à contraintes de ressources (RCPSP).

## 🚀 Installation et Utilisation Rapide

### 1. Prérequis
- Python 3.8 ou supérieur
- Aucun package externe complexe n'est requis (bibliothèque standard uniquement).

### 2. Structure du Projet
```bash
SupNum_Challenge_S3C_1447/
├── src/                # Code source
│   ├── main.py         # Point d'entrée principal
│   ├── instance.py     # Parseur d'instances J60
│   ├── genetic.py      # Algorithme Génétique
│   ├── sgs.py          # Générateur d'ordonnancement (SGS + FBI)
│   └── ns.py           # Recherche Locale (VND)
├── data/               # Dossier contenant les instances (.sm)
└── solution_j6010_8_valid.txt # Meilleure solution trouvée (Makespan 66)
```

### 3. Lancer une Résolution

Pour exécuter l'algorithme sur l'instance par défaut (`j6010_8.sm`) :

```bash
python3 src/main.py
```

Le programme affichera la progression de l'optimisation :
```text
Solving .../data/j6010_8.sm...
Loaded: Jobs=62, Resources=4, Capacities=[33, 30, 25, 26]
Initializing Population...
Starting Evolution (Target < 65)...
Gen 1: New Best Makespan = 69
Gen 5: New Best Makespan = 67
...
Final Best Makespan: 66
Solution saved to solution_j6010_8.txt
```

### 4. Vérification de la Solution

Une vérification automatique est intégrée à la fin de l'exécution. Elle confirme que :
1.  Toutes les tâches respectent l'ordre de précédence.
2.  La consommation des ressources ne dépasse jamais la capacité.

Exemple de sortie de validation :
```text
--- Verifying Solution ---
✅ Precedence Constraints: OK
✅ Resource Constraints: OK
🎉 VALID SOLUTION FOUND: Makespan 66
```

### 5. Tester une Autre Instance

Vous pouvez modifier le chemin de l'instance directement dans `src/main.py` (ligne `if __name__ == "__main__":`) ou adapter le script pour prendre un argument en ligne de commande.

---
**Groupe :** 100milliom
**Contact :** [Votre Email / GitHub]
