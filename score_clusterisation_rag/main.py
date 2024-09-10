import shutil
from extact_articles_opentargets import  extract_informations
from clusterisation import clusterisation
from select_clusters import get_cluster_texts, save_cluster_texts
from RAG.main_rag import function
import os

'''Permet de vider le repertoire qui contient les clusters pour faire l'embedding de uniquement 1 seul fichiers dans ce rep et pas tout les fichiers '''
def Empty_directory(chemin):
    for fichier in os.listdir(chemin):
        chemin_fichier = os.path.join(chemin, fichier)
        try:
            if os.path.isfile(chemin_fichier):
                os.unlink(chemin_fichier)
            elif os.path.isdir(chemin_fichier):
                shutil.rmtree(chemin_fichier)
        except Exception as e:
            print(f"Erreur lors de la suppression de {chemin_fichier}. Raison : {e}")


''' Permet de supprimer les fichiers à la fin de l'execusion du programme '''
def Delete_file(chemin_fichier):
    try:
        if os.path.exists(chemin_fichier):
            os.remove(chemin_fichier)
            print(f"Le fichier {chemin_fichier} a été supprimé avec succès.")
        else:
            print(f"Le fichier {chemin_fichier} n'existe pas.")
    except Exception as e:
        print(f"Erreur lors de la suppression de {chemin_fichier}. Raison : {e}")

            
def main():

    data_path = "titles_textes.json"  # contient les titres récuperer de europepmc et les textes récuperer le open target
    csv_file = "textes_clusters.csv" # contient les textes + titres + numéros de clusters 

    # Demander à l'utilisateur d'entrer l'identifiant de la maladie et de gène
    maladie_id = input("Entrez l'identifiant de la maladie (EFO ID) : ") #maladie_id = "MONDO_0007254"  
    gene_id = input("Entrez l'identifiant du gène (Ensembl ID) : ")#gene_id = "ENSG00000012048" 

    maladie_name=input("Entrez le nom de la maladie : ") #breast cancer
    gene_name=input("Entrez le nom du gene : ")#BRCA1


    #Appeler la fonction pour extraire les informations
    extract_informations(maladie_id, gene_id,data_path)
    
    # Appeler la fonction qui réalise la clusterisation
    clusters = clusterisation(data_path,csv_file)

    #print("Clusters retournés :", clusters)

    # Demander à l'utilisateur d'entrer le numéro de cluster qu'il souhaite garder 
    num_cluster=int(input("Entrez le numéro de cluster que vous souhiatez garder : "))
    # Recupérer les textes du clusters uniquement
    texts = get_cluster_texts(num_cluster, csv_file)
 
    # Obtenez le chemin du répertoire courant (score_clus_rag)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construisez le chemin vers le répertoire clusters
    clusters_dir = os.path.join(current_dir, 'clusters')

    # Videz le répertoire clusters
    Empty_directory(clusters_dir)

    # Sauvgarder le fichiers qui contient les clusters dans le repertoire vidé
    save_cluster_texts(texts, num_cluster)

    # Construisez le chemin vers le fichier cluster_{num_cluster}_texts.txt
    cluster_file = os.path.join(current_dir, 'clusters', f'cluster_{num_cluster}_texts.txt')
    
    # Vérifiez si le fichier existe
    if os.path.exists(cluster_file):
        # construire le prompte à envoyer à la fonction du rag
        prompt=f"the disease : {maladie_name} and the gene : {gene_name}"
        # Appelez la fonction 
        response = function(prompt, cluster_file)
    else:
        print("existe pas")
  
    print(response)
    chemin_titles_textes = os.path.join(current_dir, "titles_textes.json")
    chemin_textes_clusters = os.path.join(current_dir, "textes_clusters.csv")

    # Suppression des fichiers
    Delete_file(chemin_titles_textes)
    Delete_file(chemin_textes_clusters)



if __name__ == "__main__":
    main()
