# Analyse Intégrée des Interactions Gène-Maladie

## Description
Ce projet offre une analyse complète des interactions entre gènes et maladies, en utilisant des données provenant de diverses sources et en appliquant des techniques avancées de traitement du texte et d'apprentissage automatique.

## Fonctionnalités

1. **Récupération des Données sur les Maladies et les Gènes**
   - Collecte des scores d'évolution des maladies et des gènes associés.
   - Permet à l'utilisateur de choisir une maladie et un gène spécifiques.

2. **Intégration avec Open Targets**
   - Extrait les passages de texte pertinents mentionnant le gène et la maladie sélectionnés.
   - Collecte les identifiants de littérature pour retrouver les documents sources dans Europe PMC.

3. **Traitement des Données**
   - Génère un fichier JSON contenant :
     - Les titres des articles.
     - Les passages de texte.
     - Les identifiants de littérature (optionnel).

4. **Clusterisation des Textes**
   - Effectue une clusterisation des passages de texte extraits.
   - Produit un fichier CSV avec :
     - Les titres des articles.
     - Les passages de texte.
     - Les numéros de cluster.

5. **Analyse Pilotée par l'Utilisateur**
   - Permet à l'utilisateur de choisir un numéro de cluster spécifique.
   -  Récupère tous les textes correspondant au numéro de cluster sélectionné.

6. **Génération de Résumé basée sur RAG**
   - Applique un modèle de Génération Augmentée par Récupération (RAG) aux textes sélectionnés.
   - Utilise un prompt prédéfini, par exemple : "Rédigez un résumé de l'interaction entre le gène et la maladie suivants."
   - Génère un résumé concis des interactions gène-maladie.

## Installation

1. Clonez ce dépôt sur votre machine locale.
2. Assurez-vous d'avoir Python installé (version 3.7 ou supérieure recommandée).
3. Installez les dépendances en exécutant :
   ```bash
   pip install -r requirements.txt
## Utilisation

1. Ouvrez un terminal ou une invite de commande.
2. Naviguez vers le répertoire contenant le fichier main.py.
3. Exécutez le script avec la commande :
    ```bash
    python main.py
   python main.py
