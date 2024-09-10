
## Fonctionnalités
On récupére les scores d'évolution des maladies et les gènes associés. 
Ensuite, l'utilisateur choisit une maladie et un gène, et le programme récupère, à partir d'Open Targets, les passages dans les documents qui parlent de ce gène et de cette maladie, ainsi qu'un identifiant "id littérature" qui permet de retrouver le nom du document dont proviennent les extraits de texte dans Europe PMC. Nous obtenons ensuite un fichier JSON qui contient les titres des articles, les passages des textes et l'identifiant (optionnel).
À partir de cela, nous effectuons la clusterisation et obtenons un fichier CSV contenant les titres des articles, les passages de texte et les numéros des clusters.
L'utilisateur a la possibilité de choisir un numéro de cluster, et nous récupérons, à partir du CSV, les fichiers avant ce numéro pour leur appliquer le programme du RAG avec un prompt prédéfini, qui est par exemple : "Write the summary of the interaction between the following gene and the disease." 


## Execution
-Ouvrez un terminal ou une invite de commande.
-Naviguez vers le répertoire contenant le fichier main.py et le fichier requirements.txt.
-Installez les dépendances listées dans le fichier requirements.txt en utilisant la commande suivante : pip install -r requirements.txt
-Une fois l'installation terminée, exécutez le script avec Python en utilisant la commande suivante : python main.py
