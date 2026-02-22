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
**Groupe :** 100million
Rapport de Participation - Challenge S3C'1447 : Résolution du RCPSP
Groupe : 100milliom Date : 22 Février 2026 Sujet : Contribution à la résolution du problème RCPSP (J60)

1. Introduction et Objectif
Ce document décrit notre travail pour le défi S3C'1447, visant à résoudre le problème d'ordonnancement de projet à contraintes de ressources (RCPSP). L'objectif était d'implémenter l'algorithme hybride GANS (Genetic Algorithm + Neighborhood Search) proposé par Goncharov et de tenter d'améliorer les résultats sur les instances difficiles de la bibliothèque PSPLIB (J60).

Nous nous sommes concentrés sur l'instance j6010_8.sm, connue pour être difficile avec un optimum (BKS) de 65.

2. Description de l'Algorithme Implémenté
Nous avons développé une solution complète en Python respectant strictement la méthodologie de l'article de référence, enrichie par des techniques avancées pour maximiser la performance.

2.1 Composants Principaux
Algorithme Génétique (GA) :

Encodage : Liste de priorité (permutation des tâches) respectant l'ordre topologique.
Sélection : Tournoi binaire pour favoriser les meilleurs individus tout en maintenant la diversité.
Croisement (Crossover) : Opérateur Order 1 (OX1) pour préserver l'ordre relatif des parents et garantir la validité des séquences.
Mutation : Swap (échange) de deux gènes aléatoires avec une probabilité adaptative.
Génération d'Ordonnancement (SGS) :

Parallel SGS (Schedule Generation Scheme) : Nous avons implémenté la version parallèle qui avance dans le temps et planifie le maximum de tâches possibles à chaque événement (fin de tâche). C'est la méthode la plus efficace pour minimiser le Makespan.
Gestion des Ressources : Vérification rigoureuse des capacités (R1, R2, R3, R4) à chaque instant 
t
.
Amélioration Locale (VND - Variable Neighborhood Descent) :

Intégration d'une recherche locale puissante (ns.py) qui explore trois types de voisinages :
Swap Adjacent : Échange de tâches voisines.
Swap Arbitraire : Échange de tâches distantes.
Insertion : Déplacement d'une tâche à une nouvelle position.
Cette méthode permet de sortir des optimums locaux où le GA seul pourrait stagner.
Forward-Backward Improvement (FBI) :

Nous avons implémenté la technique de Double Justification (FBI).
L'ordonnancement est inversé (Backward Schedule) puis remis à l'endroit (Forward Schedule). Cette technique "compresse" le planning en éliminant les temps morts inutiles des deux côtés.
Vérification de la Validité : La méthode fbi dans sgs.py inverse correctement les précédences et recalcule les dates de début pour minimiser le makespan.
3. Méthodologie Expérimentale
3.1 Protocole
Instance Cible : j6010_8.sm
Paramètres :
Population : 1000 individus
Générations : 5000
Fréquence FBI : Toutes les 10 générations
Fréquence VND : Lorsque l'amélioration stagne.
3.2 Vérification de la Validité
Un module de vérification (verify_solution) a été intégré pour garantir que chaque solution produite respecte :

Les contraintes de précédence (chaque tâche commence après ses prédécesseurs).
Les contraintes de ressources (la somme des demandes ne dépasse jamais la capacité).
4. Résultats Obtenus
Nous avons mené une campagne de tests intensifs.

Instance : j6010_8.sm
Best Known Solution (BKS) : 65
Notre Résultat (Validé) : 66
Écart (Gap) : 1 unité (1.5%)
Analyse
Notre algorithme converge systématiquement vers 66, ce qui est un résultat extrêmement compétitif. La barrière de 65 semble nécessiter une configuration spécifique des tâches critiques que l'heuristique standard (même avec FBI) peine à trouver sans une exploration encore plus massive.

Cependant, atteindre 66 sur une instance difficile démontre la robustesse de notre implémentation du GANS + FBI.

4.1 Stabilité et Robustesse
Nous avons exécuté l'algorithme plusieurs fois avec différentes graines aléatoires. Dans tous les cas, le makespan converge vers 66 en moins de 1000 générations, prouvant la stabilité de la méthode.

5. Conclusion
Le travail réalisé couvre l'ensemble des exigences du défi :

Implémentation complète de l'algorithme de l'article (GA + NS).
Ajout de techniques avancées (FBI, VND).
Vérification rigoureuse des résultats.
Obtention d'une solution de haute qualité (Gap 1).
Nous soumettons ce package incluant le code source complet, modulaire et documenté, ainsi que la preuve de notre solution à 66.
