import os
import json
from datetime import datetime

def save_to_json(new_data, file_path='breast_cancer_targets.json'):

    # Vérifier si le fichier existe déjà
    if os.path.exists(file_path):
        #Si le fichier existe, il est ouvert en mode lecture ('r'), et son contenu est chargé 
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
        
        # Mettre à jour les données existantes avec les nouvelles données

        #parcourt chaque gène dans new_data["genes"]
        for new_gene_data in new_data["genes"]:
            print(f"Traitement du gène : {new_gene_data['gene_id']}")
            gene_found = False # verifie si le gene est deja present
            for existing_gene in existing_data["genes"]:
                # Si un gène avec le même gene_id est trouvé
                if new_gene_data["gene_id"] == existing_gene["gene_id"]:
                    print(f"Gène trouvé : {existing_gene['gene_id']}")
                    gene_found = True # gene_found est mis à True.
                    # Vérifier si un score avec la date actuelle existe déjà
                    today = datetime.now().strftime('%Y-%m-%d')
                    score_exists = any(score["date"] == today for score in existing_gene["scores"])
                    print(f"date existe pour : {existing_gene['gene_id']}")
                    
                    #un nouveau score est ajouté à existing_gene["scores"]
                    if not score_exists:
                        print(f"nouvelle date pour : {existing_gene['gene_id']}")
                        # Ajouter le nouveau score avec la date actuelle
                        existing_gene["scores"].append({
                            "date": today,
                            "score": new_gene_data["scores"][0]["score"]
                        })
                    break # paseer au gene suivant
            
             #le gène n'existe pas encore dans les données existantes.
            if not gene_found:
                print(f"Nouveau gène ajouté : {new_gene_data['gene_id']}")
                # Si le gène n'existe pas, l'ajouter avec le score et la date
                existing_gene_with_date = {
                    "gene_id": new_gene_data["gene_id"],
                    "approved_symbol": new_gene_data["approved_symbol"],
                    "scores": [{
                        "date": datetime.now().strftime('%Y-%m-%d'),
                        "score": new_gene_data["scores"][0]["score"]
                    }]
                }
                existing_data["genes"].append(existing_gene_with_date)# le dictionnaire est ensuite ajouté à existing_data["genes"].
    else:
        # Si le fichier n'existe pas, utiliser les nouvelles données comme base et ajouter la date
        for gene in new_data["genes"]:
            gene["scores"] = [{
                "date": datetime.now().strftime('%Y-%m-%d'),
                "score": gene["scores"][0]["score"]
            }]
        existing_data = new_data

    # Enregistrer les données mises à jour
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4) #indentation de 4 espaces

    print(f"Données enregistrées avec succès dans {file_path}")
