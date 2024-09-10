import pandas as pd
import os


'''Récupérer les textes avec le même numéro de cluster donné en paramètre'''
def get_cluster_texts(cluster_number, csv_file):
    # Charger le fichier CSV contenant les clusters et les textes
    clusters_df = pd.read_csv(csv_file)

    # Filtrer les textes associés au numéro de cluster sélectionné
    filtered_texts = clusters_df[clusters_df['Cluster'] == cluster_number]

    if not filtered_texts.empty:
        # Retourner une liste de textes associés
        return filtered_texts['Text'].tolist()
    else:
        return []  # Retourner une liste vide 
    


'''Sauvegarder les textes dans un fichier et utiliser un délimitateur qui servira à séparer les différents textes 
    et sera utilisé pour faire le découpage dans la partie RAG'''

def save_cluster_texts(texts, cluster_number):
    # Créer le répertoire clusters s'il n'existe pas
    os.makedirs("clusters", exist_ok=True)
    
    # Nom du fichier de sortie
    filename = os.path.join("clusters", f"cluster_{cluster_number}_texts.txt")
    
    # Délimiteur pour séparer les textes
    delimiter = "\n--------\n"
    
    # Enregistrer les textes dans le fichier
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(delimiter.join(texts))
    
    print(f"Les textes du cluster {cluster_number} ont été enregistrés dans le fichier '{filename}'.")
